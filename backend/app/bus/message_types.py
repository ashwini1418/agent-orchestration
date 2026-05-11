# BACKEND_AGENT | 2026-05-10 | Pydantic models for inter-agent message protocol
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.models.message import MessageType


class BaseMessage(BaseModel):
    type: MessageType
    sender: str
    target: str | None = None
    session_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InterAgentRequest(BaseMessage):
    type: Literal[MessageType.INTER_AGENT_REQUEST] = MessageType.INTER_AGENT_REQUEST
    request_body: str


class InterAgentResponse(BaseMessage):
    type: Literal[MessageType.INTER_AGENT_RESPONSE] = MessageType.INTER_AGENT_RESPONSE
    response_body: str


class ConflictMessage(BaseMessage):
    type: Literal[MessageType.CONFLICT] = MessageType.CONFLICT
    description: str
    proposed_resolution: str
    conflict_id: str = ""


class TaskCompleteMessage(BaseMessage):
    type: Literal[MessageType.TASK_COMPLETE] = MessageType.TASK_COMPLETE
    task_id: str
    summary: str


class ChangePlanMessage(BaseMessage):
    type: Literal[MessageType.CHANGE_PLAN] = MessageType.CHANGE_PLAN
    affected_agents: list[str]
    changes: dict[str, str]
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    breaking_changes: list[str] = []


class ChangeCompleteMessage(BaseMessage):
    type: Literal[MessageType.CHANGE_COMPLETE] = MessageType.CHANGE_COMPLETE


class ChangeBlockedMessage(BaseMessage):
    type: Literal[MessageType.CHANGE_BLOCKED] = MessageType.CHANGE_BLOCKED
    reason: str


class SystemMessage(BaseMessage):
    type: Literal[MessageType.SYSTEM] = MessageType.SYSTEM
    content: str
    event: str = "system"
    payload: dict[str, Any] = {}


class UserInputMessage(BaseMessage):
    type: Literal[MessageType.USER_INPUT] = MessageType.USER_INPUT
    content: str
    action: str = ""
    extra: dict[str, Any] = {}


AnyMessage = (
    InterAgentRequest
    | InterAgentResponse
    | ConflictMessage
    | TaskCompleteMessage
    | ChangePlanMessage
    | ChangeCompleteMessage
    | ChangeBlockedMessage
    | SystemMessage
    | UserInputMessage
)
