"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function AdminDepartments() {
  const { data, error } = useSWR("/department", swrFetcher);

  if (error) return <div>Error loading departments.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Departments</h1>
      {data.length === 0 ? (
        <p>No departments found.</p>
      ) : (
        data.map((dept: any) => (
          <div key={dept.id} className="p-4 border rounded-lg">
            <p>
              <strong>Name:</strong> {dept.name}
            </p>
            <p>
              <strong>Description:</strong> {dept.description}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
