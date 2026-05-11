// FRONTEND_AGENT | 2026-05-10 | Root app with routing and auth guard
import { type ReactNode, useEffect } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { authApi } from "@/api/auth";
import { useAuthStore } from "@/store/authSlice";
import { AppShell } from "@/components/layout/AppShell";
import { Spinner } from "@/components/common/Spinner";
import { LoginPage } from "@/pages/LoginPage";
import { RegisterPage } from "@/pages/RegisterPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { SessionPage } from "@/pages/SessionPage";

function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuthStore();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}

export default function App() {
  const { setUser, setLoading } = useAuthStore();

  useEffect(() => {
    setLoading(true);
    authApi
      .me()
      .then((u) => setUser(u))
      .catch(() => setUser(null));
  }, [setUser, setLoading]);

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <AppShell>
              <Routes>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/session/:id" element={<SessionPage />} />
              </Routes>
            </AppShell>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
