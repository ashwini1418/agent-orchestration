// FRONTEND_AGENT | 2026-05-10 | Zustand auth slice
import { create } from "zustand";
import type { User } from "@/types/auth";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  isAuthenticated: boolean;
}

export const useAuthStore = create<AuthState>()((set, get) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: user !== null, isLoading: false }),
  setLoading: (isLoading) => set({ isLoading }),
}));
