# BACKEND_AGENT | 2026-05-10 | AgentTask Pydantic schemas
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.models.agent_task import AgentType, TaskStatus


class AgentTaskResponse(BaseModel):
    id: str
    session_id: str
    agent_type: AgentType
    task_number: int
    status: TaskStatus
    output: str | None
    started_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}
