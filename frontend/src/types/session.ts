// FRONTEND_AGENT | 2026-05-10 | Session type definitions
export type SessionPhase =
  | "discovery"
  | "architecture"
  | "build"
  | "quality_gate"
  | "updates"
  | "complete"
  | "failed";

export interface Session {
  id: string;
  project_id: string;
  phase: SessionPhase;
  architecture_doc: string | null;
  research_brief: string | null;
  approved_at: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}
