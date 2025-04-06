"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { apiFetch } from "@/app/lib/api";
import { useRedirectFromAuthPages } from "@/app/hooks/useAuthRedirect";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();

  useRedirectFromAuthPages();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await apiFetch("/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email }),
      });
      toast.success("Password reset instructions sent to your email");
      router.push("/login");
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-4">Forgot Password</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <div>
          <label htmlFor="email" className="label">
            Email
          </label>
          <input
            type="email"
            id="email"
            className="input input-bordered w-full"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="btn btn-primary w-full"
          disabled={loading}
        >
          {loading ? "Loading..." : "Send Reset Instructions"}
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
