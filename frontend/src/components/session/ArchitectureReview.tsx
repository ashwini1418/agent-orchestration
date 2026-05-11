// FRONTEND_AGENT | 2026-05-10 | Architecture approval gate
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Button } from "@/components/common/Button";
import { Spinner } from "@/components/common/Spinner";
import type { WSClientAction } from "@/types/message";

interface Props {
  architectureDoc: string | null;
  onApprove: (action: WSClientAction, payload: Record<string, unknown>) => void;
}

export function ArchitectureReview({ architectureDoc, onApprove }: Props) {
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!architectureDoc) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-8 flex flex-col items-center gap-4">
        <Spinner size="lg" />
        <p className="text-gray-500 text-sm">Planner and Researcher agents are working...</p>
      </div>
    );
  }

  const handleApprove = async () => {
    setIsSubmitting(true);
    onApprove("approve_architecture", {});
  };

  const handleReject = async () => {
    setIsSubmitting(true);
    onApprove("reject_architecture", { feedback });
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-gray-900">Architecture Review</h3>
          <p className="text-xs text-gray-500 mt-0.5">Review the proposed architecture before build starts</p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" size="sm" onClick={() => setShowFeedback(!showFeedback)}>
            Request Changes
          </Button>
          <Button size="sm" onClick={() => void handleApprove()} isLoading={isSubmitting && !showFeedback}>
            Approve & Build ✓
          </Button>
        </div>
      </div>

      <div className="p-6 prose prose-sm max-w-none overflow-auto max-h-96">
        <ReactMarkdown>{architectureDoc}</ReactMarkdown>
      </div>

      {showFeedback && (
        <div className="px-6 pb-6 border-t border-gray-100 pt-4">
          <label htmlFor="arch-feedback" className="block text-sm font-medium text-gray-700 mb-2">
            What should be changed?
          </label>
          <textarea
            id="arch-feedback"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            rows={3}
            className="w-full rounded border border-gray-300 px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Please use PostgreSQL instead of SQLite, and add Redis for caching..."
          />
          <div className="flex justify-end gap-2 mt-3">
            <Button variant="secondary" size="sm" onClick={() => setShowFeedback(false)}>Cancel</Button>
            <Button size="sm" variant="secondary" onClick={() => void handleReject()} isLoading={isSubmitting && showFeedback}>
              Submit Feedback
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
