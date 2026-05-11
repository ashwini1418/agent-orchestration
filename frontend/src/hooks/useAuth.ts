// FRONTEND_AGENT | 2026-05-10 | Auth hook - wraps auth store + API calls
import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { authApi } from "@/api/auth";
import { useAuthStore } from "@/store/authSlice";

export function useAuth() {
  const { user, isLoading, isAuthenticated, setUser } = useAuthStore();
  const navigate = useNavigate();

  const login = useCallback(
    async (email: string, password: string) => {
      const u = await authApi.login(email, password);
      setUser(u);
      navigate("/");
    },
    [setUser, navigate]
  );

  const register = useCallback(
    async (email: string, password: string) => {
      const u = await authApi.register(email, password);
      setUser(u);
      navigate("/");
    },
    [setUser, navigate]
  );

  const logout = useCallback(async () => {
    await authApi.logout();
    setUser(null);
    navigate("/login");
  }, [setUser, navigate]);

  return { user, isLoading, isAuthenticated, login, register, logout };
}
