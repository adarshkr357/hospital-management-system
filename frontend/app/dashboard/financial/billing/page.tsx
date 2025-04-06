"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function FinancialBilling() {
  const { data, error } = useSWR("/financial/bills", swrFetcher);

  if (error) return <div>Error loading billing data.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Billing</h1>
      {data.length === 0 ? (
        <p>No billing data available.</p>
      ) : (
        data.map((bill: any) => (
          <div key={bill.id} className="p-4 border rounded-lg">
            <p>
              <strong>Patient:</strong> {bill.patient_name}
            </p>
            <p>
              <strong>Amount:</strong> {bill.amount}
            </p>
            <p>
              <strong>Status:</strong> {bill.status}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
