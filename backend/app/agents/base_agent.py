# BACKEND_AGENT | 2026-05-10 | Abstract base class for all AI agents
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from app.bus.message_bus import MessageBus
from app.bus.message_types import AnyMessage, SystemMessage, TaskCompleteMessage
from app.models.message import MessageType
from app.services import anthropic_client as llm
from app.services.file_writer import write_file


class BaseAgent(ABC):
    AGENT_TYPE: str = "base"

    def __init__(self, session_id: str, bus: MessageBus) -> None:
        self.session_id = session_id
        self.bus = bus

    @property
    @abstractmethod
    def system_prompt(self) -> str: ...

    async def emit(self, message: AnyMessage) -> None:
        await self.bus.publish(self.session_id, message)

    async def emit_system(self, event: str, content: str, payload: dict[str, Any] | None = None) -> None:
        await self.emit(
            SystemMessage(
                type=MessageType.SYSTEM,
                sender=self.AGENT_TYPE.upper(),
                session_id=self.session_id,
                content=content,
                event=event,
                payload=payload or {},
            )
        )

    async def emit_task_complete(self, task_id: str, summary: str) -> None:
        await self.emit(
            TaskCompleteMessage(
                type=MessageType.TASK_COMPLETE,
                sender=self.AGENT_TYPE.upper(),
                session_id=self.session_id,
                task_id=task_id,
                summary=summary,
            )
        )

    async def stream_llm(self, user_prompt: str, max_tokens: int = 8192) -> str:
        chunks: list[str] = []
        async for chunk in llm.stream_completion(
            system=self.system_prompt,
            user=user_prompt,
            max_tokens=max_tokens,
        ):
            chunks.append(chunk)
            await self.emit_system(
                "agent_update",
                chunk,
                {"agent": self.AGENT_TYPE, "chunk": chunk},
            )
        return "".join(chunks)

    async def write_output_file(self, relative_path: str, content: str) -> str:
        path = await write_file(self.session_id, relative_path, content)
        await self.emit_system(
            "file_written",
            f"Wrote {relative_path}",
            {"path": relative_path, "agent": self.AGENT_TYPE},
        )
        return str(path)

    @abstractmethod
    async def run(self, context: dict[str, Any]) -> str: ...
