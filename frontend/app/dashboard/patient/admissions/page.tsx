"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function PatientAdmissions() {
  const { data, error } = useSWR("/admission", swrFetcher);

  if (error) return <div>Error loading admissions data.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Admissions</h1>
      {data.length === 0 ? (
        <p>No admissions found.</p>
      ) : (
        data.map((admission: any) => (
          <div key={admission.id} className="p-4 border rounded-lg">
            <p>
              <strong>Patient: </strong> {admission.patient_name}
            </p>
            <p>
              <strong>Bed: </strong> {admission.bed_number}
            </p>
            <p>
              <strong>Status: </strong> {admission.status}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
