// FRONTEND_AGENT | 2026-05-10 | Live streaming terminal showing active agent output
import { useEffect, useRef, useCallback } from "react";
import { useSessionStore } from "@/store/sessionSlice";

const AGENT_LABELS: Record<string, string> = {
  planner: "🗺️ Planner",
  researcher: "🔬 Researcher",
  frontend: "🎨 Frontend",
  backend: "⚙️ Backend",
  database: "🗄️ Database",
  devops: "🚀 DevOps",
  update: "🔄 Update",
};

const SCROLL_THRESHOLD = 60; // px from bottom to be considered "at bottom"

export function LiveStream() {
  const { activeAgent, streamChunks, wsConnected } = useSessionStore();
  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const userScrolledUp = useRef(false);
  const prevChunkLen = useRef(0);

  const output = activeAgent ? (streamChunks[activeAgent] ?? "") : "";

  // Detect when user manually scrolls up
  const onScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    userScrolledUp.current = distanceFromBottom > SCROLL_THRESHOLD;
  }, []);

  // Auto-scroll only when new content arrives AND user is at the bottom
  useEffect(() => {
    if (output.length === prevChunkLen.current) return;
    prevChunkLen.current = output.length;
    if (!userScrolledUp.current) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [output]);

  // When agent switches, reset scroll position to bottom
  useEffect(() => {
    userScrolledUp.current = false;
    bottomRef.current?.scrollIntoView({ behavior: "instant" });
  }, [activeAgent]);

  const label = activeAgent ? (AGENT_LABELS[activeAgent] ?? activeAgent) : null;

  const scrollToBottom = () => {
    userScrolledUp.current = false;
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="bg-gray-950 rounded-xl border border-gray-800 overflow-hidden">
      {/* Terminal title bar */}
      <div className="flex items-center gap-2 px-4 py-2 bg-gray-900 border-b border-gray-800">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-red-500/70" />
          <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
          <div className="w-3 h-3 rounded-full bg-green-500/70" />
        </div>
        <div className="flex-1 text-center text-xs text-gray-400 font-mono">
          {label ? (
            <span className="flex items-center justify-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-green-400 animate-pulse" />
              {label} Agent — Live Output
            </span>
          ) : wsConnected ? (
            <span className="text-gray-500">Waiting for agent activity…</span>
          ) : (
            <span className="text-yellow-500 animate-pulse">Connecting…</span>
          )}
        </div>
        {/* Jump-to-bottom button — only shown when scrolled up */}
        <button
          onClick={scrollToBottom}
          className="w-16 text-xs text-gray-500 hover:text-gray-300 transition-colors text-right"
          title="Scroll to bottom"
        >
          ↓ bottom
        </button>
      </div>

      {/* Terminal body */}
      <div
        ref={scrollRef}
        onScroll={onScroll}
        className="h-72 overflow-y-auto p-4 font-mono text-xs leading-5"
      >
        {output ? (
          <>
            <pre className="text-green-300 whitespace-pre-wrap break-words">{output}</pre>
            {activeAgent && (
              <span className="inline-block w-2 h-4 bg-green-400 animate-pulse ml-0.5 align-middle" />
            )}
          </>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-gray-600 gap-3">
            <div className="flex gap-1">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="w-2 h-2 rounded-full bg-gray-600 animate-bounce"
                  style={{ animationDelay: `${i * 150}ms` }}
                />
              ))}
            </div>
            <p>{wsConnected ? "Agents are initialising…" : "Connecting to session…"}</p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
