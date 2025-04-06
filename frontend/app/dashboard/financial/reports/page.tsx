"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function FinancialReports() {
  const { data, error } = useSWR("/finance/reports", swrFetcher);

  if (error) return <div>Error loading reports data.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Revenue Reports</h1>
      <pre className="border rounded p-4">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
