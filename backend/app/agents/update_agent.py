# BACKEND_AGENT | 2026-05-10 | Update Agent - handles incremental change requests
from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class UpdateAgent(BaseAgent):
    AGENT_TYPE = "update"

    @property
    def system_prompt(self) -> str:
        return """You are the Update Agent. Users give you natural-language change requests and you execute them surgically.

Your process:
1. ANALYZE: What exactly needs to change? List every affected layer.
2. PLAN: Produce a Change Plan in this exact format:
   CHANGE_PLAN:
   - Affected agents: [list]
   - Changes per agent: [specific instructions for each]
   - Risk level: LOW | MEDIUM | HIGH
   - Potential breaking changes: [list or "none"]
3. CONFIRM: For MEDIUM/HIGH risk, state that user approval is required.
4. After approval (or for LOW risk), describe the exact changes each agent must make.

Be surgical - identify the minimum set of changes needed.
Always emit: CHANGE_COMPLETE or CHANGE_BLOCKED: [reason]"""

    async def run(self, context: dict[str, Any]) -> str:
        change_request = context.get("change_request", "")
        project_state = context.get("project_state", "")
        arch_doc = context.get("architecture_doc", "")

        await self.emit_system("agent_update", "Update Agent analyzing change request...", {"agent": "update"})

        prompt = f"""Current project state:
{project_state}

Current architecture:
{arch_doc}

User change request: "{change_request}"

Analyze this change, produce a Change Plan, and determine the minimum set of agents that need to act."""

        result = await self.stream_llm(prompt, max_tokens=4096)
        await self.emit_task_complete("update_plan", "Change plan produced")
        return result
