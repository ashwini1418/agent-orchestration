# BACKEND_AGENT | 2026-05-10 | Message Pydantic schemas + WebSocket envelopes
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel

from app.models.message import MessageType


class MessageResponse(BaseModel):
    id: str
    session_id: str
    message_type: MessageType
    sender: str
    target: str | None
    body: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}


class WSServerMessage(BaseModel):
    event: str
    payload: dict[str, Any]
    timestamp: datetime


class WSClientMessage(BaseModel):
    action: Literal[
        "approve_architecture",
        "reject_architecture",
        "resolve_conflict",
        "approve_change",
        "reject_change",
        "send_message",
    ]
    payload: dict[str, Any] = {}
    timestamp: datetime | None = None
