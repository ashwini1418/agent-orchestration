// FRONTEND_AGENT | 2026-05-10 | Zustand project slice
import { create } from "zustand";
import type { Project } from "@/types/project";

interface ProjectState {
  projects: Project[];
  selectedProject: Project | null;
  setProjects: (projects: Project[]) => void;
  addProject: (project: Project) => void;
  updateProject: (project: Project) => void;
  removeProject: (id: string) => void;
  selectProject: (project: Project | null) => void;
}

export const useProjectStore = create<ProjectState>()((set) => ({
  projects: [],
  selectedProject: null,
  setProjects: (projects) => set({ projects }),
  addProject: (project) => set((s) => ({ projects: [project, ...s.projects] })),
  updateProject: (project) =>
    set((s) => ({ projects: s.projects.map((p) => (p.id === project.id ? project : p)) })),
  removeProject: (id) => set((s) => ({ projects: s.projects.filter((p) => p.id !== id) })),
  selectProject: (project) => set({ selectedProject: project }),
}));
