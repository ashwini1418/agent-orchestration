"""Notification model."""
from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.database import Base
from .mixins import CUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User


class NotificationType(str, enum.Enum):
    TASK_DUE_SOON = "TASK_DUE_SOON"
    TASK_OVERDUE = "TASK_OVERDUE"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    REMINDER = "REMINDER"
    SYSTEM = "SYSTEM"
    DAILY_DIGEST = "DAILY_DIGEST"


class Notification(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type_enum"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resource_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    action_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="notifications")
