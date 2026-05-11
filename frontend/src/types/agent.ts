// FRONTEND_AGENT | 2026-05-10 | Agent task type definitions
export type AgentType =
  | "planner"
  | "researcher"
  | "frontend"
  | "backend"
  | "database"
  | "devops"
  | "update";

export type TaskStatus = "pending" | "running" | "complete" | "failed" | "blocked";

export interface AgentTask {
  id: string;
  session_id: string;
  agent_type: AgentType;
  task_number: number;
  status: TaskStatus;
  output: string | null;
  started_at: string | null;
  completed_at: string | null;
}
