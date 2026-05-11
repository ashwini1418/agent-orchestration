# DATABASE_AGENT | 2026-05-10 | Seed database with demo data
"""Run: python -m scripts.seed"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone

from app.database import AsyncSessionLocal, create_all_tables
from app.models.message import MessageType
from app.models.project import Project, ProjectStatus
from app.models.session import Session, SessionPhase
from app.models.user import User
from app.models.agent_task import AgentTask, AgentType, TaskStatus
from app.models.message import Message


async def seed() -> None:
    await create_all_tables()
    async with AsyncSessionLocal() as db:
        # Demo user
        user = User(
            id=str(uuid.uuid4()),
            email="demo@example.com",
            hashed_password=User.hash_password("demo1234"),
        )
        db.add(user)
        await db.flush()

        # Demo project
        project = Project(
            id=str(uuid.uuid4()),
            user_id=user.id,
            name="My Todo App",
            description="A fullstack todo application with tags, priorities, and team collaboration",
            status=ProjectStatus.COMPLETE,
            output_dir="./output/demo",
        )
        db.add(project)
        await db.flush()

        # Demo session
        session = Session(
            id=str(uuid.uuid4()),
            project_id=project.id,
            phase=SessionPhase.COMPLETE,
            architecture_doc="---ARCHITECTURE_START---\nProject Overview\nA fullstack todo app.\n---ARCHITECTURE_END---",
            research_brief="# Research Brief\nUse React + FastAPI + SQLite.",
            approved_at=datetime.now(timezone.utc),
        )
        db.add(session)
        await db.flush()

        # Sample messages showing inter-agent protocol
        msgs = [
            Message(session_id=session.id, message_type=MessageType.SYSTEM, sender="ORCHESTRATOR",
                    body={"content": "Starting orchestration..."}),
            Message(session_id=session.id, message_type=MessageType.TASK_COMPLETE, sender="PLANNER",
                    body={"summary": "Architecture document produced"}),
            Message(session_id=session.id, message_type=MessageType.INTER_AGENT_REQUEST,
                    sender="FRONTEND", target="BACKEND",
                    body={"request": "Need endpoint GET /api/todos returning list of todos"}),
            Message(session_id=session.id, message_type=MessageType.INTER_AGENT_RESPONSE,
                    sender="BACKEND", target="FRONTEND",
                    body={"response": "GET /api/todos implemented, returns {items: Todo[]}"}),
            Message(session_id=session.id, message_type=MessageType.TASK_COMPLETE,
                    sender="BACKEND", body={"summary": "All API routes implemented"}),
        ]
        for msg in msgs:
            db.add(msg)

        await db.commit()
        print(f"Seeded: user={user.email}, project={project.name}, session={session.id}")


if __name__ == "__main__":
    asyncio.run(seed())
