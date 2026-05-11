// FRONTEND_AGENT | 2026-05-10 | Message and WebSocket type definitions
export type MessageType =
  | "INTER_AGENT_REQUEST"
  | "INTER_AGENT_RESPONSE"
  | "CONFLICT"
  | "TASK_COMPLETE"
  | "CHANGE_PLAN"
  | "CHANGE_COMPLETE"
  | "CHANGE_BLOCKED"
  | "USER_INPUT"
  | "SYSTEM";

export interface Message {
  id: string;
  session_id: string;
  message_type: MessageType;
  sender: string;
  target: string | null;
  body: Record<string, unknown>;
  created_at: string;
}

export type WSEventType =
  | "agent_update"
  | "phase_change"
  | "conflict"
  | "architecture_ready"
  | "task_complete"
  | "build_complete"
  | "file_written"
  | "error"
  | "system";

export interface WSServerMessage {
  event: WSEventType;
  payload: Record<string, unknown>;
  timestamp: string;
}

export type WSClientAction =
  | "approve_architecture"
  | "reject_architecture"
  | "resolve_conflict"
  | "approve_change"
  | "reject_change"
  | "send_message";

export interface WSClientMessage {
  action: WSClientAction;
  payload: Record<string, unknown>;
  timestamp: string;
}
