# BACKEND_AGENT | 2026-05-10 | Sessions router - create, manage, approve orchestration sessions
from __future__ import annotations

import asyncio
import logging
import traceback
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

logger = logging.getLogger(__name__)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.middleware import get_current_user
from app.bus.message_bus import get_message_bus
from app.bus.message_types import UserInputMessage
from app.config import settings
from app.database import AsyncSessionLocal, get_db
from app.state import active_orchestrators
from app.models.agent_task import AgentTask
from app.models.message import Message, MessageType
from app.models.project import Project
from app.models.session import Session, SessionPhase
from app.models.user import User
from app.orchestrator import Orchestrator
from app.schemas.agent_task import AgentTaskResponse
from app.schemas.message import MessageResponse
from app.schemas.session import (
    ApproveArchitectureRequest,
    ConfirmChangeRequest,
    SessionResponse,
    UpdateRequest,
)

router = APIRouter(tags=["sessions"])


async def _run_orchestration(session_id: str, project_description: str) -> None:
    async with AsyncSessionLocal() as db:
        bus = get_message_bus()
        orchestrator = Orchestrator(session_id, db, bus)
        active_orchestrators[session_id] = orchestrator
        try:
            await orchestrator.run(project_description)
            await db.commit()
        except Exception as exc:
            logger.error("Orchestration failed for session %s:\n%s", session_id, traceback.format_exc())
            await db.rollback()
            # Mark session and any stuck RUNNING tasks as failed, storing the error reason
            try:
                from sqlalchemy import select as _select
                from app.models.agent_task import AgentTask, TaskStatus
                error_msg = str(exc)[:2000]

                result = await db.execute(_select(Session).where(Session.id == session_id))
                session = result.scalar_one_or_none()
                if session:
                    session.phase = SessionPhase.FAILED
                    session.error_message = error_msg

                tasks_result = await db.execute(
                    _select(AgentTask).where(
                        AgentTask.session_id == session_id,
                        AgentTask.status == TaskStatus.RUNNING,
                    )
                )
                for task in tasks_result.scalars().all():
                    task.status = TaskStatus.FAILED
                    task.output = f"Interrupted: {error_msg}"

                await db.commit()
            except Exception:
                pass
        finally:
            active_orchestrators.pop(session_id, None)


@router.post("/projects/{project_id}/sessions", response_model=SessionResponse, status_code=201)
async def create_session(
    project_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Session:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Enforce max sessions per user
    active_q = await db.execute(
        select(Session).join(Project).where(
            Project.user_id == current_user.id,
            Session.phase.notin_([SessionPhase.COMPLETE, SessionPhase.FAILED]),
        )
    )
    if len(active_q.scalars().all()) >= settings.max_sessions_per_user:
        raise HTTPException(status_code=429, detail="Maximum active sessions reached")

    session = Session(project_id=project_id)
    db.add(session)
    await db.flush()
    await db.refresh(session)
    await db.commit()  # commit before returning so GET /sessions/{id} is immediately visible

    background_tasks.add_task(_run_orchestration, session.id, project.description)
    return session


@router.get("/projects/{project_id}/sessions", response_model=list[SessionResponse])
async def list_sessions(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Session]:
    result = await db.execute(
        select(Session)
        .join(Project)
        .where(Project.id == project_id, Project.user_id == current_user.id)
        .order_by(Session.created_at.desc())
    )
    return list(result.scalars().all())


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Session:
    result = await db.execute(
        select(Session)
        .join(Project)
        .where(Session.id == session_id, Project.user_id == current_user.id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/sessions/{session_id}/approve", response_model=SessionResponse)
async def approve_session(
    session_id: str,
    body: ApproveArchitectureRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Session:
    result = await db.execute(
        select(Session)
        .join(Project)
        .where(Session.id == session_id, Project.user_id == current_user.id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    orchestrator = active_orchestrators.get(session_id)
    if orchestrator:
        action = "approve_architecture" if body.approved else "reject_architecture"
        await orchestrator.handle_user_message(
            UserInputMessage(
                type=MessageType.USER_INPUT,
                sender="USER",
                session_id=session_id,
                content=body.feedback or "",
                action=action,
                extra={"feedback": body.feedback},
            )
        )

    await db.refresh(session)
    return session


@router.post("/sessions/{session_id}/update")
async def request_update(
    session_id: str,
    body: UpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(
        select(Session)
        .join(Project)
        .where(Session.id == session_id, Project.user_id == current_user.id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.phase not in [SessionPhase.COMPLETE, SessionPhase.UPDATES]:
        raise HTTPException(status_code=400, detail="Updates only allowed after build completes")
    return {"message": "Update request received", "change_request": body.change_request}


@router.get("/sessions/{session_id}/tasks", response_model=list[AgentTaskResponse])
async def list_tasks(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[AgentTask]:
    result = await db.execute(
        select(AgentTask)
        .join(Session)
        .join(Project)
        .where(Session.id == session_id, Project.user_id == current_user.id)
        .order_by(AgentTask.task_number)
    )
    return list(result.scalars().all())


@router.get("/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def list_messages(
    session_id: str,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Message]:
    result = await db.execute(
        select(Message)
        .join(Session)
        .join(Project)
        .where(Session.id == session_id, Project.user_id == current_user.id)
        .order_by(Message.created_at)
        .offset(offset)
        .limit(limit)
    )
    return list(result.scalars().all())
