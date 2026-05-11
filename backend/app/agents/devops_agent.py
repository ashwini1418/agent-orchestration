# BACKEND_AGENT | 2026-05-10 | DevOps Agent - Docker, CI/CD, README
from __future__ import annotations

import re
from typing import Any

from app.agents.base_agent import BaseAgent

_FILE_BLOCK_RE = re.compile(r"###\s+FILE:\s+(.+?)\n```(?:\w*)?\n(.*?)```", re.DOTALL)


class DevOpsAgent(BaseAgent):
    AGENT_TYPE = "devops"

    @property
    def system_prompt(self) -> str:
        return """You are the DevOps Agent. You make the project runnable and deployable.

RULES:
- Docker images must use multi-stage builds for production.
- Never put secrets in Dockerfiles or CI config — use secret management.
- CI pipeline must run: lint → type-check → unit tests → integration tests → build.
- Write a comprehensive README with: prerequisites, local setup steps, env var reference, deployment guide.
- Local dev should start with a single command (docker-compose up).

Output files in this format:
### FILE: path/to/file
```
[file content]
```

When done: TASK_COMPLETE: devops — [list of files created]"""

    async def run(self, context: dict[str, Any]) -> str:
        arch = context.get("architecture_doc", "")
        brief = context.get("research_brief", "")
        tasks = context.get("devops_tasks", "Build Dockerfile, docker-compose, GitHub Actions CI/CD, README")

        await self.emit_system("agent_update", "DevOps Agent started - building infrastructure...", {"agent": "devops"})

        prompt = f"""Architecture Document:
{arch}

Research Brief:
{brief}

Your Tasks:
{tasks}

Build all DevOps files. Output each file using the ### FILE: path format."""

        result = await self.stream_llm(prompt, max_tokens=8192)

        for match in _FILE_BLOCK_RE.finditer(result):
            file_path = match.group(1).strip()
            content = match.group(2)
            try:
                await self.write_output_file(f"devops/{file_path}", content)
            except Exception:
                pass

        await self.emit_task_complete("devops_build", "DevOps files written")
        return result
