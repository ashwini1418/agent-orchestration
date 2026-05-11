// FRONTEND_AGENT | 2026-05-10 | Modal for resolving inter-agent conflicts
import { useState } from "react";
import { Modal } from "@/components/common/Modal";
import { Button } from "@/components/common/Button";
import { useSessionStore } from "@/store/sessionSlice";
import type { WSClientAction } from "@/types/message";

interface Props {
  onResolve: (action: WSClientAction, payload: Record<string, unknown>) => void;
}

export function ConflictModal({ onResolve }: Props) {
  const { pendingConflict, setPendingConflict } = useSessionStore();
  const [customResolution, setCustomResolution] = useState("");

  const isOpen = pendingConflict !== null;
  const conflict = pendingConflict?.payload ?? {};

  const handleAccept = () => {
    onResolve("resolve_conflict", {
      conflict_id: conflict["conflict_id"] as string,
      resolution: conflict["proposed_resolution"] as string,
    });
    setPendingConflict(null);
  };

  const handleCustom = () => {
    if (!customResolution.trim()) return;
    onResolve("resolve_conflict", {
      conflict_id: conflict["conflict_id"] as string,
      resolution: customResolution,
    });
    setPendingConflict(null);
  };

  return (
    <Modal isOpen={isOpen} onClose={() => setPendingConflict(null)} title="⚠️ Agent Conflict">
      <div className="space-y-4">
        <div className="bg-red-50 border border-red-200 rounded p-3 text-sm text-red-800">
          <strong>Conflict from {conflict["from_agent"] as string}:</strong>
          <p className="mt-1">{conflict["description"] as string}</p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded p-3 text-sm text-blue-800">
          <strong>Proposed resolution:</strong>
          <p className="mt-1">{conflict["proposed_resolution"] as string}</p>
        </div>
        <div>
          <label htmlFor="custom-res" className="block text-sm font-medium text-gray-700 mb-1">
            Or provide a custom resolution:
          </label>
          <input
            id="custom-res"
            value={customResolution}
            onChange={(e) => setCustomResolution(e.target.value)}
            className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Your custom resolution..."
          />
        </div>
        <div className="flex justify-end gap-2">
          <Button variant="secondary" size="sm" onClick={() => setPendingConflict(null)}>Dismiss</Button>
          {customResolution && (
            <Button size="sm" variant="secondary" onClick={handleCustom}>Use Custom</Button>
          )}
          <Button size="sm" onClick={handleAccept}>Accept Proposed Resolution</Button>
        </div>
      </div>
    </Modal>
  );
}
