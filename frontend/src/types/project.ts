// FRONTEND_AGENT | 2026-05-10 | Project type definitions
export type ProjectStatus = "draft" | "active" | "complete" | "failed";

export interface Project {
  id: string;
  user_id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  output_dir: string;
  created_at: string;
  updated_at: string;
  latest_session_id: string | null;
  latest_session_phase: string | null;
}

export interface CreateProjectInput {
  name: string;
  description: string;
  output_dir_name?: string;
}

export interface UpdateProjectInput {
  name?: string;
  description?: string;
}
