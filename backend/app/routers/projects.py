# BACKEND_AGENT | 2026-05-10 | Projects CRUD router
from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.middleware import get_current_user
from app.config import settings
from app.database import get_db
from app.models.project import Project
from app.models.session import Session
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ProjectResponse]:
    result = await db.execute(
        select(Project).where(Project.user_id == current_user.id).order_by(Project.created_at.desc())
    )
    projects = list(result.scalars().all())
    if not projects:
        return []

    project_ids = [p.id for p in projects]
    sessions_result = await db.execute(
        select(Session).where(Session.project_id.in_(project_ids)).order_by(Session.created_at.desc())
    )
    latest: dict[str, tuple[str, str]] = {}  # project_id -> (session_id, phase)
    for s in sessions_result.scalars().all():
        if s.project_id not in latest:
            latest[s.project_id] = (s.id, s.phase.value)

    responses = []
    for project in projects:
        r = ProjectResponse.model_validate(project)
        if project.id in latest:
            r.latest_session_id, r.latest_session_phase = latest[project.id]
        responses.append(r)
    return responses


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Project:
    dir_name = body.output_dir_name or str(uuid.uuid4())
    output_dir = str(Path(settings.output_dir).resolve() / dir_name)
    project = Project(
        user_id=current_user.id,
        name=body.name,
        description=body.description,
        output_dir=output_dir,
    )
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Project:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    body: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Project:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if body.name is not None:
        project.name = body.name
    if body.description is not None:
        project.description = body.description
    await db.flush()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
