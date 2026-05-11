# DATABASE_AGENT | 2026-05-10 | GeneratedFile ORM model
from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class GeneratedFile(UUIDMixin, Base):
    __tablename__ = "generated_files"

    session_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    agent_task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("agent_tasks.id", ondelete="CASCADE"), nullable=False
    )
    relative_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    written_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    session: Mapped[Session] = relationship("Session", back_populates="generated_files")  # type: ignore[name-defined]
    agent_task: Mapped[AgentTask] = relationship("AgentTask", back_populates="generated_files")  # type: ignore[name-defined]
