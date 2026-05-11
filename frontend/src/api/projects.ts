// FRONTEND_AGENT | 2026-05-10 | Projects API calls
import { apiDelete, apiGet, apiPatch, apiPost } from "./client";
import type { CreateProjectInput, Project, UpdateProjectInput } from "@/types/project";

export const projectsApi = {
  list: () => apiGet<Project[]>("/projects"),
  get: (id: string) => apiGet<Project>(`/projects/${id}`),
  create: (data: CreateProjectInput) => apiPost<Project>("/projects", data),
  update: (id: string, data: UpdateProjectInput) => apiPatch<Project>(`/projects/${id}`, data),
  delete: (id: string) => apiDelete(`/projects/${id}`),
};
