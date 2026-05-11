# BACKEND_AGENT | 2026-05-10 | User Pydantic schemas
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
