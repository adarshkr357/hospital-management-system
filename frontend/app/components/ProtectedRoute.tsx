// app/components/ProtectedRoute.tsx
"use client";
import { useEffect } from "react";
import { useUser } from "@/app/components/UserContext";
import { useRouter } from "next/navigation";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: string;
}

export default function ProtectedRoute({
  children,
  requiredRole,
}: ProtectedRouteProps) {
  const { user } = useUser();
  const router = useRouter();

  useEffect(() => {
    if (!user) {
      router.push("/login");
    } else if (requiredRole && user.role !== requiredRole) {
      router.push("/");
    }
  }, [user, requiredRole, router]);

  if (!user || (requiredRole && user.role !== requiredRole)) {
    return null;
  }
  return <>{children}</>;
}
