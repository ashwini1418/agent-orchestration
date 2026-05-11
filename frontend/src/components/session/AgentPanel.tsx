// FRONTEND_AGENT | 2026-05-10 | Grid of 7 agent status cards
import { useSessionStore } from "@/store/sessionSlice";
import { AgentCard } from "./AgentCard";
import type { AgentType } from "@/types/agent";

const AGENT_TYPES: AgentType[] = [
  "planner", "researcher", "frontend", "backend", "database", "devops", "update",
];

export function AgentPanel() {
  const { agentTasks, streamChunks, activeAgent } = useSessionStore();

  return (
    <section aria-label="Agent status">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Agent Status</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {AGENT_TYPES.map((type) => {
          const task = agentTasks.find((t) => t.agent_type === type) ?? null;
          return (
            <AgentCard
              key={type}
              agentType={type}
              task={task}
              streamChunk={streamChunks[type] ?? ""}
              isActive={activeAgent === type}
            />
          );
        })}
      </div>
    </section>
  );
}
