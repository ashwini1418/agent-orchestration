# BACKEND_AGENT | 2026-05-10 | Shared in-process state - active orchestrator registry
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.orchestrator.orchestrator import Orchestrator

# Maps session_id -> running Orchestrator instance
active_orchestrators: dict[str, "Orchestrator"] = {}
