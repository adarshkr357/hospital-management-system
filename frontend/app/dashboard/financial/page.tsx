"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";
import { useEnsureDashboardAccess } from "@/app/hooks/useAuthRedirect";

export default function FinancialDashboard() {
  useEnsureDashboardAccess(["ADMIN", "FINANCE"]);

  const { data, error } = useSWR("/finance/overview", swrFetcher);

  if (error) return <div>Error loading financial data.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Financial Dashboard</h1>
      <section>
        <h2 className="text-xl font-semibold">Overview</h2>
        <pre className="border rounded p-4">
          {JSON.stringify(data, null, 2)}
        </pre>
      </section>
      <div className="flex flex-wrap gap-4">
        <a href="/dashboard/financial/billing" className="btn btn-outline">
          Billing
        </a>
        <a href="/dashboard/financial/insurance" className="btn btn-outline">
          Insurance
        </a>
        <a href="/dashboard/financial/reports" className="btn btn-outline">
          Reports
        </a>
      </div>
    </div>
  );
}
