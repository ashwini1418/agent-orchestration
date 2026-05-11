# BACKEND_AGENT | 2026-05-10 | WebSocket endpoint for real-time bidirectional agent streaming
from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.auth.jwt import verify_token
from app.bus.message_bus import get_message_bus
from app.bus.message_types import SystemMessage, UserInputMessage
from app.database import AsyncSessionLocal
from app.models.message import MessageType
from app.models.project import Project
from app.models.session import Session
from app.state import active_orchestrators

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str) -> None:
    # Authenticate via HttpOnly cookie (browser sends it automatically)
    token = websocket.cookies.get("access_token", "")
    try:
        payload = verify_token(token)
        user_id: str = payload["sub"]
    except Exception:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    # Verify session belongs to user
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Session)
            .join(Project)
            .where(Session.id == session_id, Project.user_id == user_id)
        )
        if not result.scalar_one_or_none():
            await websocket.close(code=4004, reason="Session not found")
            return

    await websocket.accept()
    bus = get_message_bus()

    import asyncio

    async def _send_messages() -> None:
        async for message in bus.subscribe(session_id):
            try:
                if hasattr(message, "model_dump"):
                    data = message.model_dump(mode="json")
                    event = getattr(message, "event", message.type.value if hasattr(message, "type") else "system")
                    payload_data = getattr(message, "payload", data)
                    envelope = {
                        "event": event,
                        "payload": payload_data,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                else:
                    envelope = {
                        "event": "system",
                        "payload": str(message),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                await websocket.send_text(json.dumps(envelope))
            except Exception:
                break

    async def _receive_messages() -> None:
        while True:
            try:
                raw = await websocket.receive_text()
                data = json.loads(raw)
                action = data.get("action", "")
                orchestrator = active_orchestrators.get(session_id)
                if orchestrator:
                    await orchestrator.handle_user_message(
                        UserInputMessage(
                            type=MessageType.USER_INPUT,
                            sender="USER",
                            session_id=session_id,
                            content=json.dumps(data.get("payload", {})),
                            action=action,
                            extra=data.get("payload", {}),
                        )
                    )
            except WebSocketDisconnect:
                break
            except Exception:
                break

    send_task = asyncio.create_task(_send_messages())
    recv_task = asyncio.create_task(_receive_messages())
    try:
        done, pending = await asyncio.wait(
            [send_task, recv_task], return_when=asyncio.FIRST_COMPLETED
        )
    except Exception:
        pass
    finally:
        for t in [send_task, recv_task]:
            t.cancel()
            try:
                await t
            except (asyncio.CancelledError, Exception):
                pass
