// FRONTEND_AGENT | 2026-05-10 | Dashboard page showing all projects
import { ProjectList } from "@/components/project/ProjectList";

export function DashboardPage() {
  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Your Projects</h2>
        <p className="text-sm text-gray-500 mt-1">
          Each project runs a team of 7 AI agents that build it from scratch.
        </p>
      </div>
      <ProjectList />
    </div>
  );
}
