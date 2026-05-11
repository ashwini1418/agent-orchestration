# DATABASE_AGENT | 2026-05-10 | Session ORM model
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class SessionPhase(str, enum.Enum):
    DISCOVERY = "discovery"
    ARCHITECTURE = "architecture"
    BUILD = "build"
    QUALITY_GATE = "quality_gate"
    UPDATES = "updates"
    COMPLETE = "complete"
    FAILED = "failed"


class Session(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "sessions"

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    phase: Mapped[SessionPhase] = mapped_column(
        Enum(SessionPhase), default=SessionPhase.DISCOVERY, nullable=False
    )
    architecture_doc: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_brief: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped[Project] = relationship("Project", back_populates="sessions")  # type: ignore[name-defined]
    agent_tasks: Mapped[list[AgentTask]] = relationship(  # type: ignore[name-defined]
        "AgentTask", back_populates="session", cascade="all, delete-orphan"
    )
    messages: Mapped[list[Message]] = relationship(  # type: ignore[name-defined]
        "Message", back_populates="session", cascade="all, delete-orphan"
    )
    generated_files: Mapped[list[GeneratedFile]] = relationship(  # type: ignore[name-defined]
        "GeneratedFile", back_populates="session", cascade="all, delete-orphan"
    )
