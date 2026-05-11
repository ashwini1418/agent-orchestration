// FRONTEND_AGENT | 2026-05-10 | App-wide constants
import type { AgentType } from "@/types/agent";
import type { SessionPhase } from "@/types/session";

export const AGENT_TYPES: AgentType[] = [
  "planner", "researcher", "frontend", "backend", "database", "devops", "update",
];

export const PHASE_ORDER: SessionPhase[] = [
  "discovery", "architecture", "build", "quality_gate", "updates", "complete",
];

export const WS_RECONNECT_MAX_RETRIES = 5;
