// FRONTEND_AGENT | 2026-05-10 | Main application shell layout
import type { ReactNode } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

const routeTitles: Record<string, string> = {
  "/": "Dashboard",
};

function getTitle(pathname: string): string {
  if (pathname.startsWith("/session/")) return "Session";
  return routeTitles[pathname] ?? "Orchestrator";
}

interface AppShellProps {
  children?: ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  const { pathname } = useLocation();

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <TopBar title={getTitle(pathname)} />
        <main className="flex-1 overflow-auto p-6">{children ?? <Outlet />}</main>
      </div>
    </div>
  );
}
