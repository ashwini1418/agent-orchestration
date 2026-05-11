// FRONTEND_AGENT | 2026-05-10 | Scrolling activity log of all build events
import { useEffect, useRef, useCallback } from "react";
import { useSessionStore } from "@/store/sessionSlice";

const KIND_STYLES = {
  info: "text-gray-400",
  success: "text-green-400",
  error: "text-red-400",
  agent: "text-blue-400",
};

const SCROLL_THRESHOLD = 40;

export function ActivityLog() {
  const activityLog = useSessionStore((s) => s.activityLog);
  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const userScrolledUp = useRef(false);

  const onScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    userScrolledUp.current = distanceFromBottom > SCROLL_THRESHOLD;
  }, []);

  useEffect(() => {
    if (!userScrolledUp.current) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [activityLog.length]);

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-700">Activity Log</h3>
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-400">{activityLog.length} events</span>
          <button
            onClick={() => {
              userScrolledUp.current = false;
              bottomRef.current?.scrollIntoView({ behavior: "smooth" });
            }}
            className="text-xs text-blue-500 hover:text-blue-700"
          >
            ↓ latest
          </button>
        </div>
      </div>
      <div
        ref={scrollRef}
        onScroll={onScroll}
        className="h-48 overflow-y-auto p-3 font-mono text-xs space-y-0.5"
      >
        {activityLog.length === 0 ? (
          <p className="text-gray-400 text-center py-6">
            Activity will appear here once agents start…
          </p>
        ) : (
          activityLog.map((entry) => (
            <div key={entry.id} className="flex gap-2 leading-5">
              <span className="text-gray-500 shrink-0 select-none">{entry.ts}</span>
              <span className={KIND_STYLES[entry.kind]}>{entry.text}</span>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
