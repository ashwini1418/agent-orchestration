// FRONTEND_AGENT | 2026-05-10 | Status badge component
import type { TaskStatus } from "@/types/agent";
import type { SessionPhase } from "@/types/session";

type Color = "green" | "yellow" | "red" | "blue" | "gray" | "purple";

const colorClasses: Record<Color, string> = {
  green: "bg-green-100 text-green-800",
  yellow: "bg-yellow-100 text-yellow-800",
  red: "bg-red-100 text-red-800",
  blue: "bg-blue-100 text-blue-800",
  gray: "bg-gray-100 text-gray-800",
  purple: "bg-purple-100 text-purple-800",
};

export const taskStatusColor: Record<TaskStatus, Color> = {
  pending: "gray",
  running: "blue",
  complete: "green",
  failed: "red",
  blocked: "yellow",
};

export const phaseColor: Record<SessionPhase, Color> = {
  discovery: "gray",
  architecture: "blue",
  build: "purple",
  quality_gate: "yellow",
  updates: "blue",
  complete: "green",
  failed: "red",
};

interface BadgeProps {
  label: string;
  color?: Color;
}

export function Badge({ label, color = "gray" }: BadgeProps) {
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${colorClasses[color]}`}>
      {label}
    </span>
  );
}
