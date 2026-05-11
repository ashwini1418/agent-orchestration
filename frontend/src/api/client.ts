// FRONTEND_AGENT | 2026-05-10 | Base API client with error handling
const BASE_URL = "/api/v1";

class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new ApiError(res.status, (body as { detail?: string }).detail ?? res.statusText);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const apiGet = <T>(path: string) => request<T>(path, { method: "GET" });

export const apiPost = <T>(path: string, data?: unknown) =>
  request<T>(path, { method: "POST", body: data ? JSON.stringify(data) : undefined });

export const apiPatch = <T>(path: string, data: unknown) =>
  request<T>(path, { method: "PATCH", body: JSON.stringify(data) });

export const apiDelete = (path: string) => request<void>(path, { method: "DELETE" });

export { ApiError };
