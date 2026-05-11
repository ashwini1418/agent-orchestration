# BACKEND_AGENT | 2026-05-10 | File browsing endpoints for generated project files
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.middleware import get_current_user
from app.database import get_db
from app.models.generated_file import GeneratedFile
from app.models.project import Project
from app.models.session import Session
from app.models.user import User
from app.schemas.generated_file import FileTreeNode, GeneratedFileResponse
from app.services.file_writer import get_file_tree, resolve_safe_path

router = APIRouter(tags=["files"])


@router.get("/sessions/{session_id}/files", response_model=list[FileTreeNode])
async def get_session_file_tree(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[FileTreeNode]:
    result = await db.execute(
        select(Session)
        .join(Project)
        .where(Session.id == session_id, Project.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Session not found")
    return get_file_tree(session_id)


@router.get("/sessions/{session_id}/file-content")
async def get_file_content(
    session_id: str,
    path: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(
        select(Session)
        .join(Project)
        .where(Session.id == session_id, Project.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        full_path = resolve_safe_path(session_id, path)
        content = full_path.read_text(encoding="utf-8", errors="replace")
        return {"path": path, "content": content}
    except (FileNotFoundError, ValueError):
        raise HTTPException(status_code=404, detail="File not found")


@router.get("/sessions/{session_id}/files/{file_id}", response_model=GeneratedFileResponse)
async def get_file(
    session_id: str,
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> GeneratedFile:
    result = await db.execute(
        select(GeneratedFile)
        .join(Session)
        .join(Project)
        .where(
            GeneratedFile.id == file_id,
            GeneratedFile.session_id == session_id,
            Project.user_id == current_user.id,
        )
    )
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
