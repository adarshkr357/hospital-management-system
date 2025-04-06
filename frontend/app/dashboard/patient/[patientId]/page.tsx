"use client";
import { useParams } from "next/navigation";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function PatientDetail() {
  const params = useParams();
  const patientId = params.patientId;
  const { data, error } = useSWR(`/patient/${patientId}`, swrFetcher);

  if (error) return <div>Error loading patient details.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Patient Profile</h1>
      <section>
        <h2 className="text-xl font-semibold">Personal Details</h2>
        <pre className="border rounded p-4">
          {JSON.stringify(data, null, 2)}
        </pre>
      </section>
    </div>
  );
}
