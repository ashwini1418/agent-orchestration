// FRONTEND_AGENT | 2026-05-10 | Sessions API calls
import { apiGet, apiPost } from "./client";
import type { AgentTask } from "@/types/agent";
import type { Message } from "@/types/message";
import type { Session } from "@/types/session";

export const sessionsApi = {
  create: (projectId: string) => apiPost<Session>(`/projects/${projectId}/sessions`),
  list: (projectId: string) => apiGet<Session[]>(`/projects/${projectId}/sessions`),
  get: (sessionId: string) => apiGet<Session>(`/sessions/${sessionId}`),
  approve: (sessionId: string, approved: boolean, feedback?: string) =>
    apiPost<Session>(`/sessions/${sessionId}/approve`, { approved, feedback }),
  requestUpdate: (sessionId: string, change_request: string) =>
    apiPost(`/sessions/${sessionId}/update`, { change_request }),
  confirmChange: (sessionId: string, approved: boolean) =>
    apiPost(`/sessions/${sessionId}/confirm-change`, { approved }),
  getTasks: (sessionId: string) => apiGet<AgentTask[]>(`/sessions/${sessionId}/tasks`),
  getMessages: (sessionId: string) => apiGet<Message[]>(`/sessions/${sessionId}/messages`),
};
