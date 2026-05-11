// FRONTEND_AGENT | 2026-05-10 | Change request panel shown after build completes
import { useState } from "react";
import { useParams } from "react-router-dom";
import { Button } from "@/components/common/Button";
import { sessionsApi } from "@/api/sessions";

export function UpdatePanel() {
  const { id: sessionId } = useParams<{ id: string }>();
  const [request, setRequest] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [plan, setPlan] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!request.trim() || !sessionId) return;
    setIsSubmitting(true);
    setError("");
    try {
      const result = await sessionsApi.requestUpdate(sessionId, request) as Record<string, unknown>;
      setPlan(result);
      setRequest("");
    } catch {
      setError("Failed to submit change request");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="bg-white border border-gray-200 rounded-lg p-5" aria-label="Request changes">
      <h3 className="text-sm font-semibold text-gray-900 mb-3">Request Changes</h3>
      <p className="text-xs text-gray-500 mb-3">
        Describe a change in plain English — the Update Agent will create a Change Plan.
      </p>

      <div className="flex gap-2">
        <textarea
          value={request}
          onChange={(e) => setRequest(e.target.value)}
          rows={2}
          className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Add a dark mode toggle to the navbar..."
          aria-label="Change request"
        />
        <Button size="sm" isLoading={isSubmitting} onClick={() => void handleSubmit()}>
          Submit
        </Button>
      </div>

      {error && <p className="text-xs text-red-600 mt-2">{error}</p>}

      {plan && (
        <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded p-3 text-xs">
          <strong>Change Plan received.</strong>
          <pre className="mt-1 whitespace-pre-wrap text-gray-700">{JSON.stringify(plan, null, 2)}</pre>
        </div>
      )}
    </section>
  );
}
