# BACKEND_AGENT | 2026-05-10 | Tracks and resolves inter-agent conflicts
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.bus.message_bus import MessageBus
from app.bus.message_types import ConflictMessage, SystemMessage
from app.models.message import MessageType


class ConflictResolver:
    def __init__(self, session_id: str, bus: MessageBus) -> None:
        self.session_id = session_id
        self.bus = bus
        self._pending: dict[str, ConflictMessage] = {}
        self._resolved: dict[str, str] = {}

    def track_conflict(self, conflict: ConflictMessage) -> str:
        conflict_id = str(uuid.uuid4())
        conflict.conflict_id = conflict_id
        self._pending[conflict_id] = conflict
        return conflict_id

    def get_pending_conflicts(self) -> list[ConflictMessage]:
        return list(self._pending.values())

    def resolve_conflict(self, conflict_id: str, resolution: str) -> bool:
        if conflict_id not in self._pending:
            return False
        self._resolved[conflict_id] = resolution
        del self._pending[conflict_id]
        return True

    async def escalate_to_user(self, conflict: ConflictMessage) -> None:
        conflict_id = self.track_conflict(conflict)
        await self.bus.publish(
            self.session_id,
            SystemMessage(
                type=MessageType.SYSTEM,
                sender="ORCHESTRATOR",
                session_id=self.session_id,
                content=f"CONFLICT requires user input: {conflict.description}",
                event="conflict",
                payload={
                    "conflict_id": conflict_id,
                    "description": conflict.description,
                    "proposed_resolution": conflict.proposed_resolution,
                    "from_agent": conflict.sender,
                },
            ),
        )
