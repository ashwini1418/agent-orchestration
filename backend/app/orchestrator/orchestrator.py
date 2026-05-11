# BACKEND_AGENT | 2026-05-10 | Main orchestrator - phase state machine with parallel build agents
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents import AGENT_REGISTRY, PlannerAgent, ResearcherAgent, UpdateAgent
from app.bus.message_bus import MessageBus
from app.bus.message_types import ConflictMessage, SystemMessage, UserInputMessage
from app.database import AsyncSessionLocal
from app.models.agent_task import AgentTask, AgentType, TaskStatus
from app.models.message import MessageType
from app.models.session import Session, SessionPhase
from app.services.conflict_resolver import ConflictResolver


class Orchestrator:
    def __init__(
        self,
        session_id: str,
        db: AsyncSession,
        bus: MessageBus,
    ) -> None:
        self.session_id = session_id
        self.db = db
        self.bus = bus
        self.conflict_resolver = ConflictResolver(session_id, bus)
        self._approval_event: asyncio.Event = asyncio.Event()
        self._approval_result: dict[str, Any] = {}
        self._change_approval_event: asyncio.Event = asyncio.Event()
        self._change_approval_result: dict[str, Any] = {}

    async def _publish_system(self, event: str, content: str, payload: dict[str, Any] | None = None) -> None:
        await self.bus.publish(
            self.session_id,
            SystemMessage(
                type=MessageType.SYSTEM,
                sender="ORCHESTRATOR",
                session_id=self.session_id,
                content=content,
                event=event,
                payload=payload or {},
            ),
        )

    async def _update_phase(self, phase: SessionPhase) -> None:
        result = await self.db.execute(select(Session).where(Session.id == self.session_id))
        session = result.scalar_one_or_none()
        if session:
            session.phase = phase
            await self.db.flush()
            await self.db.commit()
        await self._publish_system("phase_change", f"Phase: {phase.value}", {"phase": phase.value})

    async def _create_task(self, agent_type: AgentType, task_number: int = 0) -> AgentTask:
        task = AgentTask(
            session_id=self.session_id,
            agent_type=agent_type,
            task_number=task_number,
            status=TaskStatus.PENDING,
        )
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task

    async def _finish_task(self, task: AgentTask, output: str, status: TaskStatus = TaskStatus.COMPLETE) -> None:
        task.status = status
        task.output = output
        task.completed_at = datetime.now(timezone.utc)
        await self.db.flush()
        await self.db.commit()

    async def handle_user_message(self, message: UserInputMessage) -> None:
        action = message.action
        if action == "approve_architecture":
            self._approval_result = {"approved": True, "feedback": message.extra.get("feedback")}
            self._approval_event.set()
        elif action == "reject_architecture":
            self._approval_result = {"approved": False, "feedback": message.extra.get("feedback")}
            self._approval_event.set()
        elif action == "approve_change":
            self._change_approval_result = {"approved": True}
            self._change_approval_event.set()
        elif action == "reject_change":
            self._change_approval_result = {"approved": False}
            self._change_approval_event.set()
        elif action == "resolve_conflict":
            conflict_id = message.extra.get("conflict_id", "")
            resolution = message.extra.get("resolution", "")
            self.conflict_resolver.resolve_conflict(conflict_id, resolution)

    async def run(self, project_description: str) -> None:
        await self._publish_system("phase_change", "Starting orchestration...", {"phase": "discovery"})

        # Phase 1: Architecture + Research (parallel)
        await self._update_phase(SessionPhase.ARCHITECTURE)
        planner_task = await self._create_task(AgentType.PLANNER, 1)
        researcher_task = await self._create_task(AgentType.RESEARCHER, 2)

        planner_task.status = TaskStatus.RUNNING
        planner_task.started_at = datetime.now(timezone.utc)
        await self.db.flush()
        await self.db.commit()  # release write lock before long LLM call

        planner = PlannerAgent(self.session_id, self.bus)
        arch_doc = await planner.run({"project_description": project_description})
        await self._finish_task(planner_task, arch_doc)

        # Update session with architecture doc
        result = await self.db.execute(select(Session).where(Session.id == self.session_id))
        session = result.scalar_one_or_none()
        if session:
            session.architecture_doc = arch_doc
            await self.db.flush()

        # Run researcher in parallel with notifying user
        researcher_task.status = TaskStatus.RUNNING
        researcher_task.started_at = datetime.now(timezone.utc)
        await self.db.flush()
        await self.db.commit()  # release write lock before long LLM call

        researcher = ResearcherAgent(self.session_id, self.bus)
        research_brief = await researcher.run({"architecture_doc": arch_doc})
        await self._finish_task(researcher_task, research_brief)

        if session:
            session.research_brief = research_brief
            await self.db.flush()

        # Signal architecture is ready for user approval
        await self._publish_system(
            "architecture_ready",
            "Architecture document ready for review",
            {"architecture_doc": arch_doc},
        )

        # Wait for user approval (timeout after 30 minutes to avoid hanging forever)
        self._approval_event.clear()
        try:
            await asyncio.wait_for(self._approval_event.wait(), timeout=1800)
        except asyncio.TimeoutError:
            raise RuntimeError("Architecture approval timed out after 30 minutes. Session expired.")
        approval = self._approval_result

        if not approval.get("approved"):
            # Re-run planner with feedback
            feedback = approval.get("feedback", "")
            await self._publish_system("phase_change", "Revising architecture...", {"phase": "architecture"})
            revised_prompt = f"{project_description}\n\nUser feedback on previous architecture:\n{feedback}"
            planner_task2 = await self._create_task(AgentType.PLANNER, 3)
            planner_task2.status = TaskStatus.RUNNING
            planner_task2.started_at = datetime.now(timezone.utc)
            await self.db.flush()
            arch_doc = await planner.run({"project_description": revised_prompt})
            await self._finish_task(planner_task2, arch_doc)
            if session:
                session.architecture_doc = arch_doc
                await self.db.flush()
            await self._publish_system(
                "architecture_ready", "Revised architecture ready", {"architecture_doc": arch_doc}
            )
            self._approval_event.clear()
            try:
                await asyncio.wait_for(self._approval_event.wait(), timeout=1800)
            except asyncio.TimeoutError:
                raise RuntimeError("Architecture approval timed out after 30 minutes. Session expired.")

        # Mark approved
        if session:
            session.approved_at = datetime.now(timezone.utc)
            await self.db.flush()

        # Phase 3: Parallel build
        await self._update_phase(SessionPhase.BUILD)
        build_agent_types = [AgentType.FRONTEND, AgentType.BACKEND, AgentType.DATABASE, AgentType.DEVOPS]
        build_tasks = [await self._create_task(at, i + 10) for i, at in enumerate(build_agent_types)]
        await self.db.commit()  # tasks must be committed before separate agent sessions can see them
        context = {
            "architecture_doc": arch_doc,
            "research_brief": research_brief,
            "project_description": project_description,
        }

        # Each build agent gets its own DB session so concurrent tasks don't
        # share an AsyncSession (SQLAlchemy forbids concurrent use of one session).
        async def run_build_agent(task_id: str, agent_type: AgentType) -> None:
            async with AsyncSessionLocal() as agent_db:
                result = await agent_db.execute(
                    select(AgentTask).where(AgentTask.id == task_id)
                )
                task = result.scalar_one_or_none()
                if not task:
                    return
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now(timezone.utc)
                await agent_db.flush()
                await agent_db.commit()  # release write lock before long LLM call

                agent_cls = AGENT_REGISTRY[agent_type]
                agent = agent_cls(self.session_id, self.bus)
                try:
                    output = await agent.run(context)
                    task.status = TaskStatus.COMPLETE
                    task.output = output
                    task.completed_at = datetime.now(timezone.utc)
                except Exception as exc:
                    task.status = TaskStatus.FAILED
                    task.output = str(exc)
                    task.completed_at = datetime.now(timezone.utc)
                finally:
                    await agent_db.flush()
                    await agent_db.commit()

        async with asyncio.TaskGroup() as tg:
            for task, agent_type in zip(build_tasks, build_agent_types):
                tg.create_task(run_build_agent(task.id, agent_type))

        # Phase 4: Quality Gate
        await self._update_phase(SessionPhase.QUALITY_GATE)
        await self._publish_system("build_complete", "All agents completed. Running quality gate.", {})

        # Mark complete
        await self._update_phase(SessionPhase.COMPLETE)
        if session:
            session.phase = SessionPhase.COMPLETE
            await self.db.flush()
        await self._publish_system("build_complete", "Project build complete!", {"phase": "complete"})
