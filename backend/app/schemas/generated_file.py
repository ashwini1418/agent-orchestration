# BACKEND_AGENT | 2026-05-10 | GeneratedFile Pydantic schemas
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class GeneratedFileResponse(BaseModel):
    id: str
    session_id: str
    agent_task_id: str
    relative_path: str
    content: str
    language: str | None
    written_at: datetime

    model_config = {"from_attributes": True}


class FileTreeNode(BaseModel):
    name: str
    path: str
    type: str  # "file" | "directory"
    children: list["FileTreeNode"] | None = None
    file_id: str | None = None
    language: str | None = None
