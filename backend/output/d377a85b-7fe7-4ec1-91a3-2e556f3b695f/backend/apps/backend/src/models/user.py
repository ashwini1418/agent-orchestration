"""User, UserProfile, and OAuthAccount models."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    ARRAY,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.database import Base
from .mixins import CUIDMixin, TimestampMixin
import enum

if TYPE_CHECKING:
    from .task import Task, Comment, AuditLog
    from .category import Category
    from .notification import Notification


class Role(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class OAuthProvider(str, enum.Enum):
    GOOGLE = "GOOGLE"
    GITHUB = "GITHUB"


class User(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role_enum"), default=Role.USER, nullable=False
    )
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_verify_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_reset_expiry: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    two_factor_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    refresh_token_hashes: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, nullable=False, server_default="{}"
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    profile: Mapped[Optional[UserProfile]] = relationship(
        "UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    tasks: Mapped[list[Task]] = relationship(
        "Task", back_populates="user", cascade="all, delete-orphan"
    )
    categories: Mapped[list[Category]] = relationship(
        "Category", back_populates="user", cascade="all, delete-orphan"
    )
    notifications: Mapped[list[Notification]] = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[list[Comment]] = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[list[AuditLog]] = relationship(
        "AuditLog", back_populates="user", cascade="all, delete-orphan"
    )


class UserProfile(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    theme: Mapped[str] = mapped_column(String(20), default="system", nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    default_view: Mapped[str] = mapped_column(String(20), default="list", nullable=False)
    notify_email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notify_push: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    daily_digest_time: Mapped[str] = mapped_column(String(5), default="08:00", nullable=False)
    week_starts_on: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="profile")


class OAuthAccount(CUIDMixin, TimestampMixin, Base):
    __tablename__ = "oauth_accounts"
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="uq_provider_user"),
    )

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[OAuthProvider] = mapped_column(
        Enum(OAuthProvider, name="oauth_provider_enum"), nullable=False
    )
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="oauth_accounts")
