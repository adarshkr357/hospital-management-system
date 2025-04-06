"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useUser } from "@/app/components/UserContext";
import toast from "react-hot-toast";
import { apiFetch } from "@/app/lib/api";
import { useRedirectFromAuthPages } from "@/app/hooks/useAuthRedirect";

export default function LoginPage() {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const { setUser } = useUser();
  const router = useRouter();

  useRedirectFromAuthPages();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      const { access_token, user_role } = data;
      localStorage.setItem("token", access_token);
      setUser({ email, role: user_role });
      toast.success("Logged in successfully!");
      // Redirect based on the user role
      if (user_role === "ADMIN") {
        router.push("/dashboard/admin");
      } else if (user_role === "STAFF") {
        router.push("/dashboard/staff");
      } else if (user_role === "FINANCE") {
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
      className="p-8 rounded shadow-xl w-full max-w-md mx-auto mt-12"
    >
      <h2 className="text-3xl font-bold mb-6 text-center text-blue-600">
        Login
      </h2>
      <div className="mb-4">
        <label htmlFor="email" className="block mb-2 font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          placeholder="Enter your email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div className="mb-6">
        <label htmlFor="password" className="block mb-2 font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          placeholder="Enter your password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200"
      >
        Login
      </button>
      <div className="mt-4 text-center text-sm">
        <a href="/forgot-password" className="text-blue-500 hover:underline">
          Forgot your password?
        </a>
      </div>
      <div className="mt-4 text-center text-sm">
        <a href="/register" className="text-blue-500 hover:underline">
          No Account? Create your own account!
        </a>
      </div>
    </form>
  );
}
