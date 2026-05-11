# BACKEND_AGENT | 2026-05-10 | Frontend Developer Agent - builds React/TypeScript UI
from __future__ import annotations

import re
from typing import Any

from app.agents.base_agent import BaseAgent


_FILE_BLOCK_RE = re.compile(
    r"###\s+FILE:\s+(.+?)\n```(?:\w+)?\n(.*?)```", re.DOTALL
)


class FrontendAgent(BaseAgent):
    AGENT_TYPE = "frontend"

    @property
    def system_prompt(self) -> str:
        return """You are the Frontend Developer Agent. You write production-grade React/TypeScript code.

RULES:
- Use TypeScript with strict mode. No `any` types.
- Follow the component hierarchy in the architecture exactly.
- Every API call must match the agreed API contract.
- Handle loading, error, and empty states for every async operation.
- Write accessible HTML (aria labels, semantic elements).
- Use Tailwind CSS for styling.
- Zustand for state management, React Router v6 for routing.

When you produce a file, output it in this format:
### FILE: path/to/file.tsx
```tsx
[file content]
```

If you need a backend endpoint that doesn't exist, emit:
INTER_AGENT_REQUEST: BACKEND_AGENT — I need endpoint [METHOD] [PATH] returning [SHAPE]. Reason: [why]

If you find an architectural conflict, emit:
CONFLICT: [description] — Proposed resolution: [your suggestion]

After all files: emit TASK_COMPLETE: frontend — [summary]"""

    async def run(self, context: dict[str, Any]) -> str:
        arch = context.get("architecture_doc", "")
        brief = context.get("research_brief", "")
        tasks = context.get("frontend_tasks", "Build all frontend components and pages")

        await self.emit_system("agent_update", "Frontend Agent started - building UI...", {"agent": "frontend"})

        prompt = f"""Architecture Document:
{arch}

Research Brief:
{brief}

Your Tasks:
{tasks}

Build all frontend files. Output each file using the ### FILE: path format."""

        result = await self.stream_llm(prompt, max_tokens=16000)

        # Parse and write any files embedded in the output
        for match in _FILE_BLOCK_RE.finditer(result):
            file_path = match.group(1).strip()
            content = match.group(2)
            try:
                await self.write_output_file(f"frontend/{file_path}", content)
            except Exception:
                pass

        await self.emit_task_complete("frontend_build", "Frontend files written")
        return result
