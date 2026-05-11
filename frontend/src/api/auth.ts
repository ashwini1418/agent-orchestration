// FRONTEND_AGENT | 2026-05-10 | Auth API calls
import { apiGet, apiPost } from "./client";
import type { User } from "@/types/auth";

export const authApi = {
  register: (email: string, password: string) =>
    apiPost<User>("/auth/register", { email, password }),

  login: (email: string, password: string) =>
    apiPost<User>("/auth/login", { email, password }),

  logout: () => apiPost<void>("/auth/logout"),

  me: () => apiGet<User>("/auth/me"),
};
