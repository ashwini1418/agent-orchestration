# DATABASE_AGENT | 2026-05-10 | AgentTask ORM model
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

try:
    from sqlalchemy import JSON
except ImportError:
    from sqlalchemy import Text as JSON  # type: ignore[assignment]


class AgentType(str, enum.Enum):
    PLANNER = "planner"
    RESEARCHER = "researcher"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    DEVOPS = "devops"
    UPDATE = "update"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    BLOCKED = "blocked"


class AgentTask(UUIDMixin, Base):
    __tablename__ = "agent_tasks"

    session_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    agent_type: Mapped[AgentType] = mapped_column(Enum(AgentType), nullable=False)
    task_number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True
    )
    input_context: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    output: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    session: Mapped[Session] = relationship("Session", back_populates="agent_tasks")  # type: ignore[name-defined]
    messages: Mapped[list[Message]] = relationship(  # type: ignore[name-defined]
        "Message", back_populates="agent_task"
    )
    generated_files: Mapped[list[GeneratedFile]] = relationship(  # type: ignore[name-defined]
        "GeneratedFile", back_populates="agent_task"
    )
