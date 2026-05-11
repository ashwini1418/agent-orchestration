// FRONTEND_AGENT | 2026-05-10 | Main session view - orchestrates all sub-components
import { useState, useEffect } from "react";
import { useSession } from "@/hooks/useSession";
import { useWebSocket } from "@/hooks/useWebSocket";
import { filesApi } from "@/api/files";
import { ProgressTracker } from "./ProgressTracker";
import { LiveStream } from "./LiveStream";
import { ActivityLog } from "./ActivityLog";
import { ArchitectureReview } from "./ArchitectureReview";
import { AgentPanel } from "./AgentPanel";
import { ConflictModal } from "./ConflictModal";
import { UpdatePanel } from "./UpdatePanel";
import { FileExplorer } from "@/components/files/FileExplorer";
import { CodeViewer } from "@/components/files/CodeViewer";
import type { FileTreeNode } from "@/types/files";
import type { WSClientAction } from "@/types/message";

interface Props {
  sessionId: string;
}

export function SessionView({ sessionId }: Props) {
  const session = useSession();
  const { sendMessage, isConnected } = useWebSocket(sessionId);
  const [selectedFile, setSelectedFile] = useState<FileTreeNode | null>(null);
  const [fileContent, setFileContent] = useState<string | null>(null);
  const [fileContentLoading, setFileContentLoading] = useState(false);

  useEffect(() => {
    if (!selectedFile || selectedFile.type !== "file") {
      setFileContent(null);
      return;
    }
    setFileContentLoading(true);
    filesApi
      .getFileContent(sessionId, selectedFile.path)
      .then((res) => setFileContent(res.content))
      .catch(() => setFileContent("// Could not load file content"))
      .finally(() => setFileContentLoading(false));
  }, [selectedFile, sessionId]);

  const handleWsAction = (action: WSClientAction, payload: Record<string, unknown>) => {
    sendMessage(action, payload);
  };

  return (
    <div className="space-y-5">
      {/* 1 — Phase stepper */}
      <ProgressTracker currentPhase={session.phase} />

      {/* 2 — WS connection badge */}
      <div className="flex items-center gap-2">
        <span
          className={`inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full ${
            isConnected ? "bg-green-50 text-green-700" : "bg-yellow-50 text-yellow-700"
          }`}
        >
          <span className={`w-1.5 h-1.5 rounded-full ${isConnected ? "bg-green-500 animate-pulse" : "bg-yellow-500"}`} />
          {isConnected ? "Live" : "Connecting…"}
        </span>
      </div>

      {/* 3 — Error banner for failed sessions */}
      {session.isFailed && session.currentSession?.error_message && (
        <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
          <span className="font-semibold">Session failed: </span>
          {session.currentSession.error_message}
        </div>
      )}

      {/* 4 — Conflict modal (overlay) */}
      <ConflictModal onResolve={handleWsAction} />

      {/* 4 — Architecture approval panel */}
      {session.showArchitectureReview && (
        <ArchitectureReview
          architectureDoc={session.currentSession?.architecture_doc ?? null}
          onApprove={handleWsAction}
        />
      )}

      {/* 5 — Live streaming terminal — always visible */}
      <LiveStream />

      {/* 6 — Agent cards + file explorer */}
      {session.showAgentPanel && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2">
            <AgentPanel />
          </div>

          {session.showFileExplorer ? (
            <div className="bg-white border border-gray-200 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Generated Files</h3>
              <FileExplorer tree={session.fileTree} onSelectFile={setSelectedFile} />
            </div>
          ) : (
            <div className="bg-gray-50 border border-dashed border-gray-200 rounded-xl p-4 flex items-center justify-center">
              <p className="text-xs text-gray-400 text-center">
                Files will appear here<br />once build starts
              </p>
            </div>
          )}
        </div>
      )}

      {/* 7 — Activity log */}
      <ActivityLog />

      {/* 8 — Code viewer for selected file */}
      {selectedFile?.type === "file" && (
        <div className="bg-gray-900 rounded-xl overflow-hidden" style={{ height: "500px" }}>
          <CodeViewer
            filePath={selectedFile.path}
            content={
              fileContentLoading
                ? "// Loading…"
                : (fileContent ?? "// Select a file from the explorer to view its content")
            }
            language={selectedFile.language}
          />
        </div>
      )}

      {/* 9 — Update request panel */}
      {session.showUpdatePanel && <UpdatePanel />}
    </div>
  );
}
