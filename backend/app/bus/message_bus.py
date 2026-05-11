# BACKEND_AGENT | 2026-05-10 | asyncio.Queue-based pub/sub message bus per session
from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import AsyncGenerator
from typing import Any


class MessageBus:
    def __init__(self) -> None:
        self._queues: dict[str, list[asyncio.Queue[Any]]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def subscribe(self, session_id: str) -> AsyncGenerator[Any, None]:
        queue: asyncio.Queue[Any] = asyncio.Queue()
        async with self._lock:
            self._queues[session_id].append(queue)
        try:
            while True:
                item = await queue.get()
                if item is None:  # sentinel = session closed
                    break
                yield item
        finally:
            async with self._lock:
                try:
                    self._queues[session_id].remove(queue)
                except ValueError:
                    pass

    async def publish(self, session_id: str, message: Any) -> None:
        async with self._lock:
            queues = list(self._queues.get(session_id, []))
        for queue in queues:
            await queue.put(message)

    async def broadcast(self, session_id: str, message: Any) -> None:
        await self.publish(session_id, message)

    async def close(self, session_id: str) -> None:
        async with self._lock:
            queues = list(self._queues.get(session_id, []))
        for queue in queues:
            await queue.put(None)  # send sentinel to all subscribers
        async with self._lock:
            self._queues.pop(session_id, None)


_bus_instance: MessageBus | None = None


def get_message_bus() -> MessageBus:
    global _bus_instance
    if _bus_instance is None:
        _bus_instance = MessageBus()
    return _bus_instance
