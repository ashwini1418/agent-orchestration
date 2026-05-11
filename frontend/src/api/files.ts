// FRONTEND_AGENT | 2026-05-10 | Files API calls
import { apiGet } from "./client";
import type { FileTreeNode } from "@/types/files";

export const filesApi = {
  getTree: (sessionId: string) => apiGet<FileTreeNode[]>(`/sessions/${sessionId}/files`),
  getFileContent: (sessionId: string, filePath: string) =>
    apiGet<{ path: string; content: string }>(
      `/sessions/${sessionId}/file-content?path=${encodeURIComponent(filePath)}`
    ),
};
