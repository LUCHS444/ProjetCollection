import type { ApiErrorBody } from "../types/api";

const API_BASE_URL = "http://localhost:8000";

export class ApiError extends Error {
  code: number;

  constructor(code: number, message: string) {
    super(message);
    this.code = code;
  }
}

function getToken(): string | null {
  return localStorage.getItem("access_token");
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return undefined as T;
  }

  const data = await response.json();

  if (!response.ok) {
    const errorBody = data as ApiErrorBody;
    const message = errorBody?.erreur?.message ?? "Une erreur est survenue";
    const code = errorBody?.erreur?.code ?? response.status;
    throw new ApiError(code, message);
  }

  return data as T;
}

export const http = {
  get: <T>(path: string) => request<T>(path, { method: "GET" }),

  post: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "POST",
      body: body !== undefined ? JSON.stringify(body) : undefined,
    }),

  patch: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "PATCH",
      body: body !== undefined ? JSON.stringify(body) : undefined,
    }),

  delete: <T>(path: string) => request<T>(path, { method: "DELETE" }),
};