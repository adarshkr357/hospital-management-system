// app/components/UserContext.tsx
"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
  JSX,
} from "react";

interface User {
  email: string;
  role: string;
}

interface UserContextProps {
  user: User | null;
  setUser: (user: User | null) => void;
  clearUser: () => void;
}

const UserContext = createContext<UserContextProps | undefined>(undefined);

export const UserProvider = ({
  children,
}: {
  children: ReactNode;
}): JSX.Element => {
  const [user, setUser] = useState<User | null>(null);

  // On initial mount, check if a token exists in localStorage.
  // If so, decode the token and, if valid, set the user accordingly.
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        // Decode the JWT token
        const base64Url = token.split(".")[1];
        const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        const jsonPayload = decodeURIComponent(
          window
            .atob(base64)
            .split("")
            .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
            .join("")
        );
        const payload = JSON.parse(jsonPayload);
        const { role, email } = payload;
        if (role) {
          setUser({ email: email || "", role });
        }
      } catch (error) {
        console.error("Failed to parse token:", error);
      }
    }
  }, []);

  const clearUser = () => {
    setUser(null);
    localStorage.removeItem("token");
  };

  return (
    <UserContext.Provider value={{ user, setUser, clearUser }}>
      {children}
    </UserContext.Provider>
  );
};

export function useUser(): UserContextProps {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}
