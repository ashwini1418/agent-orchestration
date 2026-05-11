// FRONTEND_AGENT | 2026-05-10 | Left navigation sidebar
import { NavLink } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/common/Button";

const navLinks = [
  { to: "/", label: "Dashboard", icon: "⊞" },
];

export function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="w-56 shrink-0 flex flex-col h-full bg-gray-900 text-white">
      <div className="px-4 py-5 border-b border-gray-700">
        <h1 className="text-sm font-bold text-blue-400 tracking-wide">MULTIAGENT</h1>
        <p className="text-xs text-gray-400">Orchestrator</p>
      </div>

      <nav className="flex-1 px-2 py-4 space-y-1" aria-label="Main navigation">
        {navLinks.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors
               ${isActive ? "bg-blue-700 text-white" : "text-gray-300 hover:bg-gray-700 hover:text-white"}`
            }
          >
            <span aria-hidden="true">{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-4 py-4 border-t border-gray-700">
        <p className="text-xs text-gray-400 truncate mb-2" title={user?.email}>{user?.email}</p>
        <Button variant="ghost" size="sm" onClick={() => void logout()} className="text-gray-300 w-full">
          Sign out
        </Button>
      </div>
    </aside>
  );
}
