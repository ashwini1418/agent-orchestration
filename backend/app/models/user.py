# DATABASE_AGENT | 2026-05-10 | User ORM model
from __future__ import annotations

import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    projects: Mapped[list[Project]] = relationship(  # type: ignore[name-defined]
        "Project", back_populates="user", cascade="all, delete-orphan"
    )

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password.encode())

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
