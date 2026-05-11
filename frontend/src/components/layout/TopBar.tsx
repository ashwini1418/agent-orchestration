// FRONTEND_AGENT | 2026-05-10 | Top navigation bar
import { useAuthStore } from "@/store/authSlice";
import { useSessionStore } from "@/store/sessionSlice";

interface TopBarProps {
  title: string;
}

export function TopBar({ title }: TopBarProps) {
  const user = useAuthStore((s) => s.user);
  const wsConnected = useSessionStore((s) => s.wsConnected);
  const initials = user?.email.slice(0, 2).toUpperCase() ?? "??";

  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-6 shrink-0">
      <h2 className="text-base font-semibold text-gray-800">{title}</h2>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1.5" aria-live="polite" aria-label="Connection status">
          <span
            className={`h-2 w-2 rounded-full ${wsConnected ? "bg-green-500" : "bg-gray-300"}`}
            aria-hidden="true"
          />
          <span className="text-xs text-gray-500">{wsConnected ? "Live" : "Offline"}</span>
        </div>
        <div
          className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold"
          aria-label={`User: ${user?.email ?? ""}`}
        >
          {initials}
        </div>
      </div>
    </header>
  );
}
