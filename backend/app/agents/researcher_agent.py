# BACKEND_AGENT | 2026-05-10 | Researcher Agent - produces Research Brief
from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    AGENT_TYPE = "researcher"

    @property
    def system_prompt(self) -> str:
        return """You are the Researcher Agent in a multiagent fullstack build system.
Given an architecture document, produce a comprehensive Research Brief.

Your brief MUST cover:
1. Recommended package versions (with exact install commands, security advisories)
2. Coding patterns and conventions for the chosen stack
3. Common pitfalls and how to avoid them
4. Security checklist (auth, input validation, CORS, env vars, path traversal)
5. Performance considerations (async patterns, caching, connection pooling)
6. Testing strategy (unit, integration, e2e with specific tools)

Format as structured markdown with clear sections. Be specific - include actual package names,
version numbers, and code snippets. No generic advice."""

    async def run(self, context: dict[str, Any]) -> str:
        architecture_doc = context.get("architecture_doc", "")
        await self.emit_system("agent_update", "Researcher Agent started - analyzing stack...", {"agent": "researcher"})

        prompt = f"""Given the following architecture, produce a detailed Research Brief:

{architecture_doc}

Cover all sections in your instructions with specific, actionable guidance."""

        result = await self.stream_llm(prompt, max_tokens=6144)
        await self.emit_task_complete("researcher_brief", "Research brief produced")
        return result
