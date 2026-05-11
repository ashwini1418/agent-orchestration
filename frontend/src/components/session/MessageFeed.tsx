// FRONTEND_AGENT | 2026-05-10 | Real-time scrolling message feed
import { useEffect, useRef, useCallback } from "react";
import { useSessionStore } from "@/store/sessionSlice";
import type { MessageType } from "@/types/message";

const typeColors: Record<MessageType, string> = {
  CONFLICT: "border-red-300 bg-red-50",
  TASK_COMPLETE: "border-green-300 bg-green-50",
  INTER_AGENT_REQUEST: "border-blue-300 bg-blue-50",
  INTER_AGENT_RESPONSE: "border-blue-200 bg-blue-50",
  CHANGE_PLAN: "border-yellow-300 bg-yellow-50",
  CHANGE_COMPLETE: "border-green-300 bg-green-50",
  CHANGE_BLOCKED: "border-red-300 bg-red-50",
  USER_INPUT: "border-purple-300 bg-purple-50",
  SYSTEM: "border-gray-200 bg-gray-50",
};

const SCROLL_THRESHOLD = 40;

export function MessageFeed() {
  const messages = useSessionStore((s) => s.messages);
  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const userScrolledUp = useRef(false);

  const onScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    userScrolledUp.current = el.scrollHeight - el.scrollTop - el.clientHeight > SCROLL_THRESHOLD;
  }, []);

  useEffect(() => {
    if (!userScrolledUp.current) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages.length]);

  return (
    <section aria-label="Agent messages" aria-live="polite" aria-atomic="false">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Message Feed</h3>
      <div
        ref={scrollRef}
        onScroll={onScroll}
        className="bg-white border border-gray-200 rounded-lg overflow-y-auto max-h-80 p-3 space-y-2"
      >
        {messages.length === 0 && (
          <p className="text-xs text-gray-400 text-center py-4">Messages will appear here during build...</p>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`border rounded p-2 text-xs ${typeColors[msg.message_type]}`}
          >
            <div className="flex items-center gap-2 mb-0.5">
              <span className="font-semibold text-gray-700">{msg.sender}</span>
              {msg.target && (
                <>
                  <span className="text-gray-400">→</span>
                  <span className="font-semibold text-gray-600">{msg.target}</span>
                </>
              )}
              <span className="text-gray-400 ml-auto">{msg.message_type}</span>
            </div>
            {typeof msg.body["content"] === "string" && (
              <p className="text-gray-600 truncate">{msg.body["content"] as string}</p>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </section>
  );
}
