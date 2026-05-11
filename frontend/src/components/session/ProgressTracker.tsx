// FRONTEND_AGENT | 2026-05-10 | Phase progress stepper with live status
import type { SessionPhase } from "@/types/session";

const PHASES: { key: SessionPhase; label: string; hint: string }[] = [
  { key: "discovery",     label: "Discover",     hint: "Reading requirements" },
  { key: "architecture",  label: "Architect",    hint: "Designing the system" },
  { key: "build",         label: "Build",        hint: "Agents are coding" },
  { key: "quality_gate",  label: "QA Gate",      hint: "Checking consistency" },
  { key: "complete",      label: "Complete",     hint: "Project is ready" },
];

interface Props {
  currentPhase: SessionPhase;
}

export function ProgressTracker({ currentPhase }: Props) {
  const currentIdx = PHASES.findIndex((p) => p.key === currentPhase);
  const isFailed = currentPhase === "failed";
  const activeHint = PHASES[currentIdx]?.hint ?? "";

  return (
    <nav aria-label="Build progress" className="bg-white border border-gray-200 rounded-xl p-4">
      <ol className="flex items-center">
        {PHASES.map((phase, idx) => {
          const isDone = idx < currentIdx;
          const isActive = phase.key === currentPhase;
          return (
            <li key={phase.key} className="flex items-center flex-1 min-w-0">
              <div className="flex flex-col items-center min-w-0">
                <div
                  className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold transition-all
                    ${isFailed && isActive ? "bg-red-500 text-white"
                      : isDone ? "bg-green-500 text-white"
                      : isActive ? "bg-blue-600 text-white ring-4 ring-blue-100 scale-110"
                      : "bg-gray-100 text-gray-400"}`}
                  aria-current={isActive ? "step" : undefined}
                >
                  {isDone ? "✓" : isActive && !isFailed ? (
                    <span className="flex gap-0.5">
                      <span className="w-1 h-1 rounded-full bg-white animate-bounce" style={{ animationDelay: "0ms" }} />
                      <span className="w-1 h-1 rounded-full bg-white animate-bounce" style={{ animationDelay: "150ms" }} />
                      <span className="w-1 h-1 rounded-full bg-white animate-bounce" style={{ animationDelay: "300ms" }} />
                    </span>
                  ) : idx + 1}
                </div>
                <span className={`text-xs mt-1.5 font-medium whitespace-nowrap ${isActive ? "text-blue-600" : isDone ? "text-green-600" : "text-gray-400"}`}>
                  {phase.label}
                </span>
              </div>
              {idx < PHASES.length - 1 && (
                <div className={`flex-1 h-0.5 mx-2 mb-5 transition-colors ${idx < currentIdx ? "bg-green-400" : "bg-gray-200"}`} />
              )}
            </li>
          );
        })}
      </ol>

      {!isFailed && activeHint && (
        <p className="text-xs text-blue-600 mt-3 text-center font-medium animate-pulse">
          {activeHint}…
        </p>
      )}
      {isFailed && (
        <p className="text-xs text-red-600 mt-3 text-center font-medium">Build failed</p>
      )}
    </nav>
  );
}
