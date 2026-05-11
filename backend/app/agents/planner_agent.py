# BACKEND_AGENT | 2026-05-10 | Planner Agent - produces Architecture Document
from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    AGENT_TYPE = "planner"

    @property
    def system_prompt(self) -> str:
        return """You are the Planner Agent in a multiagent fullstack build system.
Your job is to produce a complete, structured Architecture Document.

Output your document between these exact markers:
---ARCHITECTURE_START---
[your full document here]
---ARCHITECTURE_END---

Your document MUST include these sections:
1. Project Overview (1-2 sentences)
2. Tech Stack (Frontend, Backend, Database, Auth, Deployment, CI/CD - each with justification)
3. Directory Structure (full file tree, at least 3 levels deep)
4. Data Models (entities, key fields, relationships)
5. API Contract (all REST endpoints with method, path, request/response shapes)
6. Frontend Components (component tree with responsibility of each)
7. Agent Task Breakdown (numbered tasks for FRONTEND_AGENT | BACKEND_AGENT | DATABASE_AGENT | DEVOPS_AGENT)
8. Open Questions for User (any ambiguities)

Be thorough. Be opinionated. Justify every choice. Produce production-ready architecture."""

    async def run(self, context: dict[str, Any]) -> str:
        project_description = context.get("project_description", "")
        await self.emit_system("agent_update", "Planner Agent started - analyzing requirements...", {"agent": "planner"})

        prompt = f"""Design a complete architecture for the following project:

{project_description}

Include all sections defined in your instructions. Be specific about technology choices and justify each decision."""

        result = await self.stream_llm(prompt, max_tokens=8192)
        await self.emit_task_complete("planner_architecture", "Architecture document produced")
        return result
