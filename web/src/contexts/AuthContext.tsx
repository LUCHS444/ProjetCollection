import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { http, ApiError } from "../services/http";
import type { UserRead, Token, UserLogin, UserCreate } from "../types/api";

interface AuthContextValue {
  user: UserRead | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (data: UserLogin) => Promise<void>;
  register: (data: UserCreate) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem("access_token")
  );
  const [user, setUser] = useState<UserRead | null>(null);

  // Vérifie le token auprès de l'API : charge l'utilisateur, ou déconnecte si le token est refusé
  useEffect(() => {
    if (!token) {
      return;
    }
    let annule = false;

    http
      .get<UserRead>("/auth/me")
      .then((me) => {
        if (!annule) {
          setUser(me);
        }
      })
      .catch((err: unknown) => {
        if (!annule && err instanceof ApiError && err.code === 401) {
          localStorage.removeItem("access_token");
          setToken(null);
          setUser(null);
        }
      });

    return () => {
      annule = true;
    };
  }, [token]);

  async function login(data: UserLogin): Promise<void> {
    const response = await http.post<Token>("/auth/login", data);
    localStorage.setItem("access_token", response.access_token);
    setToken(response.access_token);
  }

  async function register(data: UserCreate): Promise<void> {
    await http.post<UserRead>("/auth/register", data);
    await login({ email: data.email, password: data.password });
  }

  function logout(): void {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  }

  const value: AuthContextValue = {
    user,
    token,
    isAuthenticated: token !== null,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth doit être utilisé à l'intérieur d'un AuthProvider");
  }
  return context;
}