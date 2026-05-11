# DATABASE_AGENT | 2026-05-10 | Project ORM model
from __future__ import annotations

import enum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETE = "complete"
    FAILED = "failed"


class Project(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "projects"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False
    )
    output_dir: Mapped[str] = mapped_column(String(500), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="projects")  # type: ignore[name-defined]
    sessions: Mapped[list[Session]] = relationship(  # type: ignore[name-defined]
        "Session", back_populates="project", cascade="all, delete-orphan"
    )
