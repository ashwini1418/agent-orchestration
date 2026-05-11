# BACKEND_AGENT | 2026-05-10 | Database Agent - schema, migrations, seed data
from __future__ import annotations

import re
from typing import Any

from app.agents.base_agent import BaseAgent

_FILE_BLOCK_RE = re.compile(r"###\s+FILE:\s+(.+?)\n```(?:\w+)?\n(.*?)```", re.DOTALL)


class DatabaseAgent(BaseAgent):
    AGENT_TYPE = "database"

    @property
    def system_prompt(self) -> str:
        return """You are the Database Agent. You own the entire data layer.

RULES:
- Every schema change is a versioned migration file. No raw ALTER TABLE in application code.
- All migrations must be reversible (up + down).
- Add appropriate indexes for all foreign keys and frequently queried fields.
- When responding to an INTER_AGENT_REQUEST for a schema change:
  * Assess if the change is backward-compatible
  * If breaking: emit CONFLICT before making it
  * If safe: emit the migration file and TASK_COMPLETE
- Include seed data for at least one realistic dev scenario.

Output files in this format:
### FILE: path/to/file.py
```python
[file content]
```

When done: TASK_COMPLETE: database — [schema changes, migration file names]"""

    async def run(self, context: dict[str, Any]) -> str:
        arch = context.get("architecture_doc", "")
        brief = context.get("research_brief", "")
        tasks = context.get("database_tasks", "Build all schema migrations and seed data")

        await self.emit_system("agent_update", "Database Agent started - building schema...", {"agent": "database"})

        prompt = f"""Architecture Document:
{arch}

Research Brief:
{brief}

Your Tasks:
{tasks}

Build all database migration files and seed data. Output each file using the ### FILE: path format."""

        result = await self.stream_llm(prompt, max_tokens=8192)

        for match in _FILE_BLOCK_RE.finditer(result):
            file_path = match.group(1).strip()
            content = match.group(2)
            try:
                await self.write_output_file(f"database/{file_path}", content)
            except Exception:
                pass

        await self.emit_task_complete("database_build", "Database files written")
        return result
