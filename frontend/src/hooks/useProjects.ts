// FRONTEND_AGENT | 2026-05-10 | Projects hook - React Query + store sync
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { projectsApi } from "@/api/projects";
import { useProjectStore } from "@/store/projectSlice";
import type { CreateProjectInput } from "@/types/project";

export function useProjects() {
  const qc = useQueryClient();
  const { setProjects, addProject, removeProject } = useProjectStore();

  const { data: projects = [], isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: async () => {
      const list = await projectsApi.list();
      setProjects(list);
      return list;
    },
  });

  const createMutation = useMutation({
    mutationFn: (data: CreateProjectInput) => projectsApi.create(data),
    onSuccess: (project) => {
      addProject(project);
      void qc.invalidateQueries({ queryKey: ["projects"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => projectsApi.delete(id),
    onSuccess: (_, id) => {
      removeProject(id);
      void qc.invalidateQueries({ queryKey: ["projects"] });
    },
  });

  return {
    projects,
    isLoading,
    createProject: createMutation.mutateAsync,
    deleteProject: deleteMutation.mutateAsync,
    isCreating: createMutation.isPending,
  };
}
