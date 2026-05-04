import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { message } from "antd";
import { authApi } from "./api/authApi";
import { tokenStorage } from "../../lib/auth/tokenStorage";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => tokenStorage.getToken());
  const [user, setUser] = useState(() => tokenStorage.getUser());
  const [isHydrating, setIsHydrating] = useState(Boolean(tokenStorage.getToken()));

  useEffect(() => {
    if (!token) {
      setIsHydrating(false);
      return;
    }

    let ignore = false;
    authApi
      .me()
      .then((nextUser) => {
        if (ignore) {
          return;
        }
        setUser(nextUser);
        tokenStorage.setUser(nextUser);
      })
      .catch(() => {
        if (ignore) {
          return;
        }
        tokenStorage.clearAll();
        setToken(null);
        setUser(null);
      })
      .finally(() => {
        if (!ignore) {
          setIsHydrating(false);
        }
      });

    return () => {
      ignore = true;
    };
  }, [token]);

  const value = useMemo(
    () => ({
      token,
      user,
      isAuthenticated: Boolean(token && user),
      isHydrating,
      async login(credentials) {
        const response = await authApi.login(credentials);
        const nextToken = response.access_token;
        const nextUser = {
          username: response.username,
          role: response.role,
        };

        tokenStorage.setToken(nextToken);
        tokenStorage.setUser(nextUser);
        setToken(nextToken);
        setUser(nextUser);
        message.success("Login admin berhasil");
        return nextUser;
      },
      logout() {
        tokenStorage.clearAll();
        setToken(null);
        setUser(null);
        message.success("Anda telah logout");
      },
    }),
    [isHydrating, token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
