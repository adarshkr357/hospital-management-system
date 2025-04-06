"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function PatientAppointments() {
  const { data, error } = useSWR("/appointment", swrFetcher);

  if (error) return <div>Error loading appointments.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Appointments</h1>

      {data.length === 0 ? (
        <p>No appointments found.</p>
      ) : (
        data.map((appointment: any) => (
          <div key={appointment.id} className="p-4 border rounded-lg">
            <p>
              <strong>Date: </strong> {appointment.appointment_date}
            </p>
            <p>
              <strong>Status: </strong> {appointment.status}
            </p>
            <p>
              <strong>Purpose: </strong> {appointment.purpose}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
