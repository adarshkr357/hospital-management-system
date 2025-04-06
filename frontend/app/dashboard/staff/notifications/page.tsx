"use client";
import useSWR from "swr";
import { swrFetcher } from "@/app/lib/api";
import LoadingSpinner from "@/app/components/LoadingSpinner";

export default function StaffNotifications() {
  const { data, error } = useSWR("/notification", swrFetcher);

  if (error) return <div>Error loading notifications.</div>;
  if (!data) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Notifications</h1>
      {data.length === 0 ? (
        <p>No notifications found.</p>
      ) : (
        data.map((notification: any) => (
          <div key={notification.id} className="p-4 border rounded-lg">
            <p>{notification.message}</p>
            <p className="text-xs">
              {new Date(notification.created_at).toLocaleString()}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
