// app/components/ThemeContext.tsx
"use client";
import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
  JSX
} from "react";

interface ThemeContextProps {
  theme: string;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextProps | undefined>(undefined);

export function ThemeProvider({
  children,
}: {
  children: ReactNode;
}): JSX.Element {
  const [theme, setTheme] = useState<string>("light");

  useEffect(() => {
    const savedTheme: string | null = localStorage.getItem("theme");
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute("data-theme", savedTheme);
    } else {
      document.documentElement.setAttribute("data-theme", theme);
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "forest" : "light";
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
    document.documentElement.setAttribute("data-theme", newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextProps {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
