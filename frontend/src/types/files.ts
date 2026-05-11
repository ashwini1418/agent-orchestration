// FRONTEND_AGENT | 2026-05-10 | File tree type definitions
export interface GeneratedFile {
  id: string;
  session_id: string;
  agent_task_id: string;
  relative_path: string;
  content: string;
  language: string | null;
  written_at: string;
}

export interface FileTreeNode {
  name: string;
  path: string;
  type: "file" | "directory";
  children?: FileTreeNode[];
  file_id?: string;
  language?: string;
}
