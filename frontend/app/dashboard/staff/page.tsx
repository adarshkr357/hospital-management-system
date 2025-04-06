"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";
import { useEnsureDashboardAccess } from "@/app/hooks/useAuthRedirect";

export default function StaffDashboard() {
  useEnsureDashboardAccess(["ADMIN", "FINANCE", "STAFF"]);

  const { data, error } = useSWR("/staff", swrFetcher);

  if (error) return <div>Error loading staff roster.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Staff Dashboard</h1>
      <section>
        <h2 className="text-xl font-semibold">Staff Roster</h2>
        {data.length === 0 ? (
          <p>No staff data available.</p>
        ) : (
          data.map((staff: any) => (
            <div key={staff.id} className="p-4 border rounded-lg">
              <p>
                <strong>Name: </strong> {staff.full_name}
              </p>
              <p>
                <strong>Role: </strong> {staff.role}
              </p>
              <p>
                <strong>Department: </strong> {staff.department_name}
              </p>
            </div>
          ))
        )}
      </section>
      <div className="flex flex-wrap gap-4">
        <a href="/dashboard/staff/attendance" className="btn btn-outline">
          Attendance
        </a>
        <a href="/dashboard/staff/schedule" className="btn btn-outline">
          Schedule
        </a>
        <a href="/dashboard/staff/notifications" className="btn btn-outline">
          Notifications
        </a>
      </div>
    </div>
  );
}
