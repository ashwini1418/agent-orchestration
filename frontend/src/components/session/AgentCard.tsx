// FRONTEND_AGENT | 2026-05-10 | Individual agent status card
import { Badge, taskStatusColor } from "@/components/common/Badge";
import type { AgentTask, AgentType } from "@/types/agent";

const agentEmoji: Record<AgentType, string> = {
  planner: "🗺️",
  researcher: "🔬",
  frontend: "🎨",
  backend: "⚙️",
  database: "🗄️",
  devops: "🚀",
  update: "🔄",
};

interface Props {
  agentType: AgentType;
  task: AgentTask | null;
  streamChunk: string;
  isActive: boolean;
}

export function AgentCard({ agentType, task, streamChunk, isActive }: Props) {
  const status = task?.status ?? "pending";
  const label = agentType.charAt(0).toUpperCase() + agentType.slice(1);
  const preview = streamChunk.slice(-300) || task?.output?.slice(-300) || "";
  const hasOutput = preview.length > 0;

  return (
    <div
      className={`bg-white border rounded-xl p-4 transition-all ${
        isActive
          ? "border-blue-400 shadow-md shadow-blue-100"
          : status === "complete"
          ? "border-green-200"
          : status === "failed"
          ? "border-red-200"
          : "border-gray-200"
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-xl" aria-hidden="true">{agentEmoji[agentType]}</span>
          <span className="font-medium text-sm text-gray-900">{label}</span>
        </div>
        <div className="flex items-center gap-1.5">
          {isActive && (
            <span className="inline-block w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
          )}
          <Badge label={status} color={taskStatusColor[status]} />
        </div>
      </div>

      {hasOutput && (
        <pre className="mt-2 text-xs text-gray-500 bg-gray-50 rounded-lg p-2 max-h-28 overflow-auto whitespace-pre-wrap break-words leading-4">
          {preview}
          {isActive && (
            <span className="inline-block w-1.5 h-3 bg-blue-400 animate-pulse ml-0.5 align-middle" />
          )}
        </pre>
      )}

      {!hasOutput && status === "pending" && (
        <p className="text-xs text-gray-400 mt-1">Waiting…</p>
      )}
    </div>
  );
}
