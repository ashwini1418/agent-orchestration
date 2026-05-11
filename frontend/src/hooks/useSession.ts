// FRONTEND_AGENT | 2026-05-10 | Session hook - derives UI state from phase
import { useSessionStore } from "@/store/sessionSlice";
import type { SessionPhase } from "@/types/session";

const PHASE_ORDER: SessionPhase[] = [
  "discovery",
  "architecture",
  "build",
  "quality_gate",
  "updates",
  "complete",
];

export function useSession() {
  const store = useSessionStore();
  const phase = store.currentSession?.phase ?? "discovery";

  const phaseIndex = PHASE_ORDER.indexOf(phase);
  const isAfter = (p: SessionPhase) => phaseIndex > PHASE_ORDER.indexOf(p);
  const isCurrent = (p: SessionPhase) => phase === p;

  return {
    ...store,
    phase,
    phaseIndex,
    showArchitectureReview: isCurrent("architecture"),
    showAgentPanel: phase !== "failed",
    showFileExplorer: isAfter("build") || phase === "complete",
    showUpdatePanel: phase === "complete" || phase === "updates",
    isComplete: phase === "complete",
    isFailed: phase === "failed",
    isBuilding: phase === "build",
  };
}
