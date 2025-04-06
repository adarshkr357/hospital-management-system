"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { apiFetch } from "@/app/lib/api";
import { useUser } from "@/app/components/UserContext";
import { useRedirectFromAuthPages } from "@/app/hooks/useAuthRedirect";

export default function RegisterPage() {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [role, setRole] = useState<string>("PATIENT");
  const [loading, setLoading] = useState<boolean>(false);
  const { setUser } = useUser();
  const router = useRouter();

  useRedirectFromAuthPages();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password, role }),
      });
      const { access_token, user_role } = data;
      localStorage.setItem("token", access_token);
      setUser({ email, role: user_role });
      toast.success("Registration successful!");
      if (role === "ADMIN") {
        router.push("/dashboard/admin");
      } else if (role === "STAFF") {
        router.push("/dashboard/staff");
      } else if (role === "FINANCE") {
        router.push("/dashboard/financial");
      } else {
        router.push("/dashboard/patient");
      }
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-8 rounded shadow-md w-full max-w-md mx-auto mt-12"
    >
      <h2 className="text-3xl font-bold mb-6 text-center text-blue-600">
        Register
      </h2>
      <div className="mb-4">
        <label htmlFor="email" className="block mb-2 font-medium">
          Email
        </label>
        <input
          type="email"
          id="email"
          placeholder="Enter your email"
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div className="mb-4">
        <label htmlFor="password" className="block mb-2 font-medium">
          Password
        </label>
        <input
          type="password"
          id="password"
          placeholder="Enter your password"
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <div className="mb-6">
        <label htmlFor="role" className="block mb-2 font-medium">
          Role
        </label>
        <select
          id="role"
          className="select select-bordered w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="PATIENT">Patient</option>
          <option value="STAFF">Staff</option>
          <option value="ADMIN">Admin</option>
          <option value="FINANCE">Finance</option>
        </select>
      </div>
      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200 ease-in-out mb-4"
        disabled={loading}
      >
        {loading ? "Loading..." : "Register"}
      </button>
      <div className="text-center text-sm">
        <a href="/login" className="text-blue-500 hover:underline">
          Already have an account? Login here.
        </a>
      </div>
    </form>
  );
}
