"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function FinancialInsurance() {
  const { data, error } = useSWR("/finance/insurance-claims", swrFetcher);

  if (error) return <div>Error loading insurance claims.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Insurance Claims</h1>
      {data.length === 0 ? (
        <p>No insurance claims available.</p>
      ) : (
        data.map((claim: any) => (
          <div key={claim.id} className="p-4 border rounded-lg">
            <p>
              <strong>Patient:</strong> {claim.patient_name}
            </p>
            <p>
              <strong>Claim Amount:</strong> {claim.claim_amount}
            </p>
            <p>
              <strong>Status:</strong> {claim.status}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
