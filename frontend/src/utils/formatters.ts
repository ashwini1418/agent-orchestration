// FRONTEND_AGENT | 2026-05-10 | Utility formatting functions
import type { SessionPhase } from "@/types/session";
import type { AgentType } from "@/types/agent";

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export function formatRelativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60_000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return formatDate(iso);
}

export function truncateText(text: string, maxLength: number): string {
  return text.length > maxLength ? text.slice(0, maxLength) + "…" : text;
}

export const agentTypeToLabel: Record<AgentType, string> = {
  planner: "Planner",
  researcher: "Researcher",
  frontend: "Frontend",
  backend: "Backend",
  database: "Database",
  devops: "DevOps",
  update: "Update",
};

export const phaseToLabel: Record<SessionPhase, string> = {
  discovery: "Discovery",
  architecture: "Architecture Review",
  build: "Building",
  quality_gate: "Quality Gate",
  updates: "Updates",
  complete: "Complete",
  failed: "Failed",
};
