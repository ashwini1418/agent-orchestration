"""User profile request/response schemas."""
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UpdateProfileRequest(BaseModel):
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    bio: Optional[str] = Field(default=None, max_length=500)
    timezone: Optional[str] = Field(default=None, max_length=50)
    theme: Optional[str] = Field(default=None, pattern="^(light|dark|system)$")
    language: Optional[str] = Field(default=None, max_length=10)
    default_view: Optional[str] = Field(default=None, pattern="^(list|kanban|calendar)$")
    notify_email: Optional[bool] = None
    notify_push: Optional[bool] = None
    daily_digest_time: Optional[str] = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    week_starts_on: Optional[int] = Field(default=None, ge=0, le=6)


class UserProfileResponse(BaseModel):
    id: str
    user_id: str
    display_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    timezone: str
    theme: str
    language: str
    default_view: str
    notify_email: bool
    notify_push: bool
    daily_digest_time: str
    week_starts_on: int

    model_config = {"from_attributes": True}


class FullUserResponse(BaseModel):
    id: str
    email: str
    username: str
    role: str
    is_email_verified: bool
    two_factor_enabled: bool
    last_login_at: Optional[str] = None
    profile: Optional[UserProfileResponse] = None

    model_config = {"from_attributes": True}
