# BACKEND_AGENT | 2026-05-10 | Project Pydantic schemas
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.project import ProjectStatus


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=10, max_length=10_000)
    output_dir_name: str = Field(default="", pattern=r"^[a-zA-Z0-9_\-]{0,64}$")


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=10, max_length=10_000)


class ProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    status: ProjectStatus
    output_dir: str
    created_at: datetime
    updated_at: datetime
    latest_session_id: str | None = None
    latest_session_phase: str | None = None

    model_config = {"from_attributes": True}
