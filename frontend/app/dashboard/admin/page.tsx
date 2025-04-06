"use client";
import { useUser } from "@/app/components/UserContext";
import { useEnsureDashboardAccess } from "@/app/hooks/useAuthRedirect";

export default function AdminDashboard() {
  const { user } = useUser();

  useEnsureDashboardAccess("ADMIN");

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Admin Dashboard</h1>
      <p>Welcome, {user?.email}</p>
      <div className="flex flex-wrap gap-4">
        <a href="/dashboard/admin/departments" className="btn btn-outline">
          Departments
        </a>
        <a href="/dashboard/admin/users" className="btn btn-outline">
          User Management
        </a>
      </div>
    </div>
  );
}
