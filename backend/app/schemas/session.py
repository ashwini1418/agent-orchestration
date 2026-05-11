# BACKEND_AGENT | 2026-05-10 | Session Pydantic schemas
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.session import SessionPhase


class SessionResponse(BaseModel):
    id: str
    project_id: str
    phase: SessionPhase
    architecture_doc: str | None
    research_brief: str | None
    approved_at: datetime | None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApproveArchitectureRequest(BaseModel):
    approved: bool
    feedback: str | None = Field(default=None, max_length=5000)


class UpdateRequest(BaseModel):
    change_request: str = Field(min_length=10, max_length=5000)


class ConfirmChangeRequest(BaseModel):
    approved: bool
