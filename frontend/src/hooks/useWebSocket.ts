// FRONTEND_AGENT | 2026-05-10 | WebSocket hook with auto-reconnect and event dispatch
import { useCallback, useEffect, useRef, useState } from "react";
import { useSessionStore } from "@/store/sessionSlice";
import { filesApi } from "@/api/files";
import type { WSClientAction, WSServerMessage } from "@/types/message";

const MAX_RETRIES = 5;
const BASE_DELAY_MS = 1000;

const AGENT_LABELS: Record<string, string> = {
  planner: "🗺️ Planner",
  researcher: "🔬 Researcher",
  frontend: "🎨 Frontend",
  backend: "⚙️ Backend",
  database: "🗄️ Database",
  devops: "🚀 DevOps",
  update: "🔄 Update",
};

const PHASE_LABELS: Record<string, string> = {
  discovery: "Discovery — analyzing requirements",
  architecture: "Architecture — designing the system",
  build: "Build — agents are coding",
  quality_gate: "Quality Gate — checking consistency",
  complete: "Complete — your project is ready",
  failed: "Failed",
  updates: "Updates — applying changes",
};

// Access store imperatively to avoid stale closures and re-render loops.
// Calling useSessionStore.getState() inside callbacks always gets the latest
// state without subscribing the hook to every store change.
const getStore = () => useSessionStore.getState();

export function useWebSocket(sessionId: string | null) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastEvent, setLastEvent] = useState<WSServerMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const retriesRef = useRef(0);
  const lastAgentRef = useRef<string | null>(null);
  const sessionIdRef = useRef(sessionId);
  // Track whether the hook is still mounted to avoid state updates after unmount
  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  useEffect(() => {
    sessionIdRef.current = sessionId;
  }, [sessionId]);

  const dispatch = useCallback((msg: WSServerMessage) => {
    setLastEvent(msg);
    const store = getStore();
    const { event, payload } = msg;
    const ev = (event ?? "").toLowerCase();

    if (ev === "phase_change" && typeof payload["phase"] === "string") {
      const phase = payload["phase"] as string;
      store.updatePhase(phase as never);
      store.addActivity(`Phase → ${PHASE_LABELS[phase] ?? phase}`, "info");

    } else if (ev === "agent_update") {
      const agent = (payload["agent"] as string | undefined) ?? "unknown";
      const chunk = (payload["chunk"] as string | undefined) ?? "";
      store.appendChunk(agent, chunk);
      if (lastAgentRef.current !== agent) {
        lastAgentRef.current = agent;
        store.addActivity(`${AGENT_LABELS[agent] ?? agent} agent is working…`, "agent");
      }

    } else if (ev === "task_complete" || ev === "TASK_COMPLETE") {
      const summary = (payload["summary"] as string | undefined) ?? "";
      const taskId = (payload["task_id"] as string | undefined) ?? "";
      store.addActivity(`✓ ${taskId}: ${summary}`, "success");
      store.setActiveAgent(null);
      lastAgentRef.current = null;

    } else if (ev === "conflict") {
      store.setPendingConflict(msg);
      const desc = (payload["description"] as string | undefined) ?? "Conflict detected";
      store.addActivity(`⚠ Conflict: ${desc}`, "error");

    } else if (ev === "architecture_ready") {
      const archDoc = payload["architecture_doc"] as string | undefined;
      const current = store.currentSession;
      if (archDoc && current) {
        store.setSession({ ...current, architecture_doc: archDoc });
      }
      store.addActivity("✓ Architecture ready — waiting for your approval", "success");
      store.setActiveAgent(null);
      lastAgentRef.current = null;

    } else if (ev === "build_complete") {
      store.updatePhase("complete");
      store.addActivity("🎉 Build complete! All agents finished.", "success");
      store.setActiveAgent(null);
      lastAgentRef.current = null;
      const sid = sessionIdRef.current;
      if (sid) {
        filesApi.getTree(sid).then((tree) => getStore().setFileTree(tree)).catch(() => {});
      }

    } else if (ev === "file_written") {
      const path = (payload["path"] as string | undefined) ?? "";
      if (path) store.addActivity(`  📄 ${path}`, "info");

    } else if (ev === "system" || ev === "SYSTEM") {
      const content = (payload["content"] as string | undefined) ?? JSON.stringify(payload);
      if (content) store.addActivity(content, "info");

    } else if (ev === "inter_agent_request" || ev === "INTER_AGENT_REQUEST") {
      const body = (payload["request_body"] as string | undefined) ?? "";
      const sender = (payload["sender"] as string | undefined) ?? "agent";
      const target = (payload["target"] as string | undefined) ?? "agent";
      store.addActivity(`↔ ${sender} → ${target}: ${body.slice(0, 120)}`, "info");
    }
  }, []); // No store dependency — uses getStore() imperatively

  const connect = useCallback(() => {
    if (!sessionId) return;
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const url = `${proto}://${window.location.host}/ws/${sessionId}`;
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      if (!mountedRef.current) return;
      setIsConnected(true);
      retriesRef.current = 0;
      getStore().setWsConnected(true);
      getStore().addActivity("Connected — agents are starting…", "info");
    };

    ws.onmessage = (ev: MessageEvent<string>) => {
      try {
        const msg = JSON.parse(ev.data) as WSServerMessage;
        dispatch(msg);
      } catch {
        // malformed message
      }
    };

    ws.onclose = () => {
      if (!mountedRef.current) return;
      setIsConnected(false);
      getStore().setWsConnected(false);
      if (retriesRef.current < MAX_RETRIES) {
        const delay = BASE_DELAY_MS * 2 ** retriesRef.current;
        retriesRef.current += 1;
        getStore().addActivity(`Reconnecting in ${Math.round(delay / 1000)}s…`, "error");
        setTimeout(connect, delay);
      }
    };

    ws.onerror = () => ws.close();
  }, [sessionId, dispatch]); // stable: sessionId changes on page nav, dispatch is stable

  useEffect(() => {
    retriesRef.current = 0;
    connect();
    return () => {
      wsRef.current?.close();
    };
  }, [connect]);

  const sendMessage = useCallback(
    (action: WSClientAction, payload: Record<string, unknown> = {}) => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(
          JSON.stringify({ action, payload, timestamp: new Date().toISOString() })
        );
      }
    },
    []
  );

  return { isConnected, sendMessage, lastEvent };
}
