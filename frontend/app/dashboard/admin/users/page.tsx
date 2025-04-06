"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function AdminUsers() {
  const { data, error } = useSWR("/admin/users", swrFetcher);

  if (error) return <div>Error loading users.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">User Management</h1>
      {data.length === 0 ? (
        <p>No users found.</p>
      ) : (
        data.map((user: any) => (
          <div key={user.id} className="p-4 border rounded-lg">
            <p>
              <strong>Email:</strong> {user.email}
            </p>
            <p>
              <strong>Role:</strong> {user.role}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
