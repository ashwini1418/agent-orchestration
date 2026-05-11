# DATABASE_AGENT | 2026-05-10 | Message ORM model for inter-agent communication
from __future__ import annotations

import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

try:
    from sqlalchemy import JSON
except ImportError:
    from sqlalchemy import Text as JSON  # type: ignore[assignment]

from sqlalchemy import DateTime, func


class MessageType(str, enum.Enum):
    INTER_AGENT_REQUEST = "INTER_AGENT_REQUEST"
    INTER_AGENT_RESPONSE = "INTER_AGENT_RESPONSE"
    CONFLICT = "CONFLICT"
    TASK_COMPLETE = "TASK_COMPLETE"
    CHANGE_PLAN = "CHANGE_PLAN"
    CHANGE_COMPLETE = "CHANGE_COMPLETE"
    CHANGE_BLOCKED = "CHANGE_BLOCKED"
    USER_INPUT = "USER_INPUT"
    SYSTEM = "SYSTEM"


class Message(UUIDMixin, Base):
    __tablename__ = "messages"

    session_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    agent_task_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("agent_tasks.id", ondelete="SET NULL"), nullable=True
    )
    message_type: Mapped[MessageType] = mapped_column(Enum(MessageType), nullable=False)
    sender: Mapped[str] = mapped_column(String(50), nullable=False)
    target: Mapped[str | None] = mapped_column(String(50), nullable=True)
    body: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    session: Mapped[Session] = relationship("Session", back_populates="messages")  # type: ignore[name-defined]
    agent_task: Mapped[AgentTask | None] = relationship("AgentTask", back_populates="messages")  # type: ignore[name-defined]
