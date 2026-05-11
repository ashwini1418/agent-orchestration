// FRONTEND_AGENT | 2026-05-10 | Session page - loads session data and renders SessionView
import { useEffect } from "react";
import { useParams, Navigate } from "react-router-dom";
import { sessionsApi } from "@/api/sessions";
import { filesApi } from "@/api/files";
import { useSessionStore } from "@/store/sessionSlice";
import { SessionView } from "@/components/session/SessionView";
import { Spinner } from "@/components/common/Spinner";
import { ErrorBoundary } from "@/components/common/ErrorBoundary";

export function SessionPage() {
  const { id } = useParams<{ id: string }>();
  const { currentSession, setSession, setTasks, setFileTree, reset } = useSessionStore();

  useEffect(() => {
    if (!id) return;
    reset();

    const load = async () => {
      const [session, tasks] = await Promise.all([
        sessionsApi.get(id),
        sessionsApi.getTasks(id),
      ]);
      setSession(session);
      setTasks(tasks);
      if (session.phase === "complete" || session.phase === "updates") {
        filesApi.getTree(id).then(setFileTree).catch(() => {});
      }
    };

    void load();
  }, [id, reset, setSession, setTasks, setFileTree]);

  if (!id) return <Navigate to="/" replace />;

  if (!currentSession) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-1">Build Session</h2>
        <p className="text-xs text-gray-400 mb-6 font-mono">{id}</p>
        <SessionView sessionId={id} />
      </div>
    </ErrorBoundary>
  );
}
