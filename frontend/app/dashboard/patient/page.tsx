"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";
import { useEnsureDashboardAccess } from "@/app/hooks/useAuthRedirect";

export default function PatientDashboard() {
  useEnsureDashboardAccess(["ADMIN", "FINANCE", "STAFF", "PATIENT"]);

  const { data, error } = useSWR("/patient", swrFetcher);

  console.log(`Error: ${error}`);

  if (error) return <div>Error loading patient data.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Patient Dashboard</h1>
      <section>
        <h2 className="text-xl font-semibold">Patient Records</h2>
        <pre className="border rounded p-4">
          {JSON.stringify(data, null, 2)}
        </pre>
      </section>
      <div className="flex flex-wrap gap-4">
        <a href="/dashboard/patient/appointments" className="btn btn-outline">
          Appointments
        </a>
        <a href="/dashboard/patient/admissions" className="btn btn-outline">
          Admissions
        </a>
        <a href="/dashboard/patient/communication" className="btn btn-outline">
          Communication
        </a>
      </div>
    </div>
  );
}
