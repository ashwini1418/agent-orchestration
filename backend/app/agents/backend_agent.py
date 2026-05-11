# BACKEND_AGENT | 2026-05-10 | Backend Developer Agent - builds FastAPI server code
from __future__ import annotations

import re
from typing import Any

from app.agents.base_agent import BaseAgent

_FILE_BLOCK_RE = re.compile(r"###\s+FILE:\s+(.+?)\n```(?:\w+)?\n(.*?)```", re.DOTALL)


class BackendAgent(BaseAgent):
    AGENT_TYPE = "backend"

    @property
    def system_prompt(self) -> str:
        return """You are the Backend Developer Agent. You write production-grade FastAPI/Python code.

RULES:
- Implement every endpoint in the API contract. Do not deviate without emitting a CONFLICT.
- Validate all inputs with Pydantic schemas.
- Never expose stack traces or internal errors to clients.
- Use environment variables for all secrets — never hardcode.
- All database access uses SQLAlchemy async sessions.

Output files in this format:
### FILE: path/to/file.py
```python
[file content]
```

For schema changes: INTER_AGENT_REQUEST: DATABASE_AGENT — I need [change]. Reason: [why]
For conflicts: CONFLICT: [description] — Proposed resolution: [suggestion]
When done: TASK_COMPLETE: backend — [summary]"""

    async def run(self, context: dict[str, Any]) -> str:
        arch = context.get("architecture_doc", "")
        brief = context.get("research_brief", "")
        tasks = context.get("backend_tasks", "Build all API routes, agents, and orchestrator")

        await self.emit_system("agent_update", "Backend Agent started - building API...", {"agent": "backend"})

        prompt = f"""Architecture Document:
{arch}

Research Brief:
{brief}

Your Tasks:
{tasks}

Build all backend files. Output each file using the ### FILE: path format."""

        result = await self.stream_llm(prompt, max_tokens=16000)

        for match in _FILE_BLOCK_RE.finditer(result):
            file_path = match.group(1).strip()
            content = match.group(2)
            try:
                await self.write_output_file(f"backend/{file_path}", content)
            except Exception:
                pass

        await self.emit_task_complete("backend_build", "Backend files written")
        return result
