"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function StaffSchedule() {
  const { data, error } = useSWR("/staff/schedule", swrFetcher);

  if (error) return <div>Error loading schedule data.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Schedule</h1>
      {data.length === 0 ? (
        <p>No schedule details available.</p>
      ) : (
        data.map((schedule: any) => (
          <div key={schedule.id} className="p-4 border rounded-lg">
            <p>
              <strong>Staff:</strong> {schedule.full_name}
            </p>
            <p>
              <strong>Shift:</strong> {schedule.shift_start} -{" "}
              {schedule.shift_end}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
