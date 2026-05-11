// FRONTEND_AGENT | 2026-05-10 | Zustand session slice - drives real-time UI state
import { create } from "zustand";
import type { AgentTask } from "@/types/agent";
import type { Message, WSServerMessage } from "@/types/message";
import type { Session, SessionPhase } from "@/types/session";
import type { FileTreeNode } from "@/types/files";

interface ActivityEntry {
  id: string;
  ts: string;
  text: string;
  kind: "info" | "success" | "error" | "agent";
}

interface SessionState {
  currentSession: Session | null;
  agentTasks: AgentTask[];
  messages: Message[];
  streamChunks: Record<string, string>;
  fileTree: FileTreeNode[];
  wsConnected: boolean;
  pendingConflict: WSServerMessage | null;
  changePlan: WSServerMessage | null;
  activityLog: ActivityEntry[];
  activeAgent: string | null;

  setSession: (session: Session) => void;
  updatePhase: (phase: SessionPhase) => void;
  addMessage: (message: Message) => void;
  updateTask: (task: AgentTask) => void;
  setTasks: (tasks: AgentTask[]) => void;
  appendChunk: (agent: string, chunk: string) => void;
  setFileTree: (tree: FileTreeNode[]) => void;
  setWsConnected: (connected: boolean) => void;
  setPendingConflict: (msg: WSServerMessage | null) => void;
  setChangePlan: (msg: WSServerMessage | null) => void;
  addActivity: (text: string, kind?: ActivityEntry["kind"]) => void;
  setActiveAgent: (agent: string | null) => void;
  reset: () => void;
}

let _logId = 0;

export const useSessionStore = create<SessionState>()((set) => ({
  currentSession: null,
  agentTasks: [],
  messages: [],
  streamChunks: {},
  fileTree: [],
  wsConnected: false,
  pendingConflict: null,
  changePlan: null,
  activityLog: [],
  activeAgent: null,

  setSession: (session) => set({ currentSession: session }),
  updatePhase: (phase) =>
    set((s) =>
      s.currentSession ? { currentSession: { ...s.currentSession, phase } } : {}
    ),
  addMessage: (message) =>
    set((s) => ({ messages: [...s.messages, message] })),
  updateTask: (task) =>
    set((s) => ({
      agentTasks: s.agentTasks.some((t) => t.id === task.id)
        ? s.agentTasks.map((t) => (t.id === task.id ? task : t))
        : [...s.agentTasks, task],
    })),
  setTasks: (tasks) => set({ agentTasks: tasks }),
  appendChunk: (agent, chunk) =>
    set((s) => ({
      activeAgent: agent,
      streamChunks: {
        ...s.streamChunks,
        [agent]: (s.streamChunks[agent] ?? "") + chunk,
      },
    })),
  setFileTree: (fileTree) => set({ fileTree }),
  setWsConnected: (wsConnected) => set({ wsConnected }),
  setPendingConflict: (pendingConflict) => set({ pendingConflict }),
  setChangePlan: (changePlan) => set({ changePlan }),
  addActivity: (text, kind = "info") =>
    set((s) => ({
      activityLog: [
        ...s.activityLog,
        {
          id: String(++_logId),
          ts: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
          text,
          kind,
        },
      ].slice(-200),
    })),
  setActiveAgent: (activeAgent) => set({ activeAgent }),
  reset: () =>
    set({
      currentSession: null,
      agentTasks: [],
      messages: [],
      streamChunks: {},
      fileTree: [],
      wsConnected: false,
      pendingConflict: null,
      changePlan: null,
      activityLog: [],
      activeAgent: null,
    }),
}));
