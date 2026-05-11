# BACKEND_AGENT | 2026-05-10 | Safe async file writer with directory traversal prevention
from __future__ import annotations

import asyncio
from pathlib import Path

import aiofiles

from app.config import settings
from app.schemas.generated_file import FileTreeNode

_BASE = Path(settings.output_dir).resolve()
_file_locks: dict[str, asyncio.Lock] = {}


def resolve_safe_path(session_id: str, relative_path: str) -> Path:
    candidate = (_BASE / session_id / relative_path).resolve()
    if not candidate.is_relative_to(_BASE):
        raise ValueError(f"Path traversal attempt: {relative_path!r}")
    return candidate


async def write_file(session_id: str, relative_path: str, content: str) -> Path:
    path = resolve_safe_path(session_id, relative_path)
    key = str(path)
    if key not in _file_locks:
        _file_locks[key] = asyncio.Lock()
    async with _file_locks[key]:
        path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(content)
    return path


def _build_tree(base: Path, root: Path) -> list[FileTreeNode]:
    nodes: list[FileTreeNode] = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    except PermissionError:
        return nodes
    for entry in entries:
        rel = entry.relative_to(base).as_posix()
        if entry.is_dir():
            nodes.append(
                FileTreeNode(
                    name=entry.name,
                    path=rel,
                    type="directory",
                    children=_build_tree(base, entry),
                )
            )
        else:
            ext = entry.suffix.lstrip(".")
            nodes.append(
                FileTreeNode(name=entry.name, path=rel, type="file", language=ext or None)
            )
    return nodes


def get_file_tree(session_id: str) -> list[FileTreeNode]:
    session_dir = (_BASE / session_id).resolve()
    if not session_dir.exists():
        return []
    return _build_tree(session_dir, session_dir)
