"use client";

import { useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { apiFetch } from "@/app/lib/api";
import { useRedirectFromAuthPages } from "@/app/hooks/useAuthRedirect";

// This is the Suspense fallback component
const SuspenseFallback = () => <div>Loading...</div>;

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<SuspenseFallback />}>
      <ResetPasswordForm />
    </Suspense>
  );
}

function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const token: string = searchParams.get("token") || "";
  const [newPassword, setNewPassword] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();

  useRedirectFromAuthPages();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await apiFetch("/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({ token, new_password: newPassword }),
      });
      toast.success("Password reset successful. Please log in.");
      router.push("/login");
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-4">Reset Password</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <div>
          <label htmlFor="newPassword" className="label">
            New Password
          </label>
          <input
            type="password"
            id="newPassword"
            className="input input-bordered w-full"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="btn btn-primary w-full"
          disabled={loading}
        >
          {loading ? "Loading..." : "Reset Password"}
        </button>
      </form>
      <div className="mt-4">
        <a href="/login" className="link">
          Back to Login
        </a>
      </div>
    </div>
  );
}
