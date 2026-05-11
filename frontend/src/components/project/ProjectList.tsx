// FRONTEND_AGENT | 2026-05-10 | Grid of project cards with new project button
import { useState } from "react";
import { useProjects } from "@/hooks/useProjects";
import { ProjectCard } from "./ProjectCard";
import { NewProjectModal } from "./NewProjectModal";
import { Button } from "@/components/common/Button";
import { Spinner } from "@/components/common/Spinner";

export function ProjectList() {
  const { projects, isLoading } = useProjects();
  const [isModalOpen, setIsModalOpen] = useState(false);

  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-sm text-gray-500">
          {projects.length === 0 ? "No projects yet" : `${projects.length} project${projects.length !== 1 ? "s" : ""}`}
        </p>
        <Button onClick={() => setIsModalOpen(true)}>+ New Project</Button>
      </div>

      {projects.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          <p className="text-4xl mb-4">🤖</p>
          <p className="text-lg font-medium">No projects yet</p>
          <p className="text-sm mt-1">Create a project to start building with AI agents</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}

      <NewProjectModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}
