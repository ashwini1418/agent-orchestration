# BACKEND_AGENT | 2026-05-10 | FastAPI app factory - lifespan, routers, middleware
from __future__ import annotations

import logging
import traceback
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import AsyncSessionLocal, create_all_tables
from app.routers import projects, sessions, ws, files
from app.auth.router import router as auth_router

logger = logging.getLogger(__name__)


async def _cleanup_orphaned_sessions() -> None:
    """Mark any RUNNING sessions/tasks as FAILED on startup (left over from a crash/reload)."""
    from sqlalchemy import select, update
    from app.models.agent_task import AgentTask, TaskStatus
    from app.models.session import Session, SessionPhase

    async with AsyncSessionLocal() as db:
        try:
            # Tasks stuck as RUNNING
            await db.execute(
                update(AgentTask)
                .where(AgentTask.status == TaskStatus.RUNNING)
                .values(status=TaskStatus.FAILED, output="Server restarted while task was running")
            )
            # Sessions stuck in non-terminal phase
            terminal = [SessionPhase.COMPLETE, SessionPhase.FAILED]
            result = await db.execute(
                select(Session).where(Session.phase.notin_(terminal))
            )
            orphaned = result.scalars().all()
            for s in orphaned:
                s.phase = SessionPhase.FAILED
                s.error_message = "Server restarted while session was running"
            await db.commit()
            if orphaned:
                logger.warning("Cleaned up %d orphaned session(s) on startup", len(orphaned))
        except Exception:
            logger.exception("Failed to clean up orphaned sessions on startup")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_all_tables()
    await _cleanup_orphaned_sessions()
    yield


app = FastAPI(
    title="Multiagent Orchestrator API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Cookie"],
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception on %s %s:\n%s", request.method, request.url.path, traceback.format_exc())
    detail = f"{type(exc).__name__}: {exc}" if settings.debug else "Internal server error"
    return JSONResponse(status_code=500, content={"detail": detail})


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(files.router, prefix="/api/v1")
app.include_router(ws.router)
