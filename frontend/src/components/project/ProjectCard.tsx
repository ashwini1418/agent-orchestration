// FRONTEND_AGENT | 2026-05-10 | Project card with status badge and navigation
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Badge } from "@/components/common/Badge";
import { sessionsApi } from "@/api/sessions";
import type { Project } from "@/types/project";

interface ProjectCardProps {
  project: Project;
}

const TERMINAL_PHASES = ["complete", "failed"];

export function ProjectCard({ project }: ProjectCardProps) {
  const navigate = useNavigate();
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const statusColor = project.status === "complete" ? "green" : project.status === "failed" ? "red" : project.status === "active" ? "blue" : "gray";

  const latestSessionId = project.latest_session_id;
  const latestPhase = project.latest_session_phase;
  const hasActiveSession = latestSessionId && latestPhase && !TERMINAL_PHASES.includes(latestPhase);
  const hasTerminalSession = latestSessionId && latestPhase && TERMINAL_PHASES.includes(latestPhase);

  const startSession = async () => {
    setStarting(true);
    setError(null);
    try {
      const session = await sessionsApi.create(project.id);
      navigate(`/session/${session.id}`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to start session");
      setStarting(false);
    }
  };

  return (
    <article className="bg-white rounded-lg border border-gray-200 p-5 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-gray-900 truncate flex-1">{project.name}</h3>
        <Badge label={project.status} color={statusColor} />
      </div>
      <p className="text-sm text-gray-500 line-clamp-2 mb-4">{project.description}</p>
      {error && <p className="text-xs text-red-500 mb-2">{error}</p>}
      <div className="flex items-center justify-between">
        <time className="text-xs text-gray-400" dateTime={project.created_at}>
          {new Date(project.created_at).toLocaleDateString()}
        </time>
        <div className="flex items-center gap-3">
          {hasTerminalSession && (
            <Link
              to={`/session/${latestSessionId}`}
              className="text-xs text-gray-400 hover:text-gray-600"
            >
              View last
            </Link>
          )}
          {hasActiveSession ? (
            <Link
              to={`/session/${latestSessionId}`}
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              Open session →
            </Link>
          ) : (
            <button
              onClick={() => void startSession()}
              disabled={starting}
              className="text-sm text-gray-500 hover:text-blue-600 font-medium disabled:opacity-50"
            >
              {starting ? "Starting…" : "Start session →"}
            </button>
          )}
        </div>
      </div>
    </article>
  );
}
