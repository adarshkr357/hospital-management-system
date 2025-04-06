"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function StaffAttendance() {
  const { data, error } = useSWR("/staff/attendance", swrFetcher);

  if (error) return <div>Error loading attendance data.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Attendance</h1>
      {data.length === 0 ? (
        <p>No attendance records available.</p>
      ) : (
        data.map((record: any) => (
          <div key={record.id} className="p-4 border rounded-lg">
            <p>
              <strong>Date:</strong> {record.date}
            </p>
            <p>
              <strong>Status:</strong> {record.status}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
