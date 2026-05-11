"""Task, SubTask, Tag, Attachment, Comment, and AuditLog models."""
from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.database import Base
from .mixins import CUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .category import Category


class Priority(str, enum.Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
    CANCELLED = "CANCELLED"


class Task(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "tasks"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    parent_task_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority, name="priority_enum"), default=Priority.NONE, nullable=False
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status_enum"), default=TaskStatus.TODO, nullable=False
    )
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sort_order: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    reminder_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    recurrence_rule: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="tasks")
    category: Mapped[Optional[Category]] = relationship("Category", back_populates="tasks")
    tags: Mapped[list[TaskTag]] = relationship(
        "TaskTag", back_populates="task", cascade="all, delete-orphan"
    )
    subtasks: Mapped[list[SubTask]] = relationship(
        "SubTask", back_populates="task", cascade="all, delete-orphan"
    )
    attachments: Mapped[list[Attachment]] = relationship(
        "Attachment", back_populates="task", cascade="all, delete-orphan"
    )
    comments: Mapped[list[Comment]] = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[list[AuditLog]] = relationship(
        "AuditLog", back_populates="task", cascade="all, delete-orphan"
    )
    parent_task: Mapped[Optional[Task]] = relationship(
        "Task", remote_side="Task.id", back_populates="child_tasks"
    )
    child_tasks: Mapped[list[Task]] = relationship(
        "Task", back_populates="parent_task"
    )


class Tag(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_tag_name"),)

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(7), default="#6366f1", nullable=False)

    task_tags: Mapped[list[TaskTag]] = relationship("TaskTag", back_populates="tag")


class TaskTag(Base):
    __tablename__ = "task_tags"
    __table_args__ = (UniqueConstraint("task_id", "tag_id", name="uq_task_tag"),)

    task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    task: Mapped[Task] = relationship("Task", back_populates="tags")
    tag: Mapped[Tag] = relationship("Tag", back_populates="task_tags")


class SubTask(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "subtasks"

    task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    task: Mapped[Task] = relationship("Task", back_populates="subtasks")


class Attachment(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "attachments"

    task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_key: Mapped[str] = mapped_column(String(500), nullable=False)  # S3 key
    file_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    task: Mapped[Task] = relationship("Task", back_populates="attachments")


class Comment(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "comments"

    task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    task: Mapped[Task] = relationship("Task", back_populates="comments")
    user: Mapped[User] = relationship("User", back_populates="comments")


class AuditLog(CUIDMixin, Base):
    __tablename__ = "audit_logs"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    task_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    old_values: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    new_values: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    user: Mapped[User] = relationship("User", back_populates="audit_logs")
    task: Mapped[Optional[Task]] = relationship("Task", back_populates="audit_logs")
