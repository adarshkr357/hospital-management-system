// app/components/Navbar.tsx
"use client";
import Link from "next/link";
import { useUser } from "@/app/components/UserContext";
import ThemeToggle from "@/app/components/ThemeToggle";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const { user, clearUser } = useUser();
    const router = useRouter();

  return (
    <nav className="navbar bg-base-200 shadow-md">
      <div className="flex-1">
        <Link href="/" className="btn btn-ghost normal-case text-xl">
          Hospital Management
        </Link>
      </div>
      <div className="flex items-center space-x-4">
        {user ? (
          <>
            <span className="hidden sm:inline-block">{user.email}</span>
            <button
              className="btn btn-sm"
              onClick={() => {
                clearUser();
                router.push("/");
              }}
            >
              Sign Out
            </button>
          </>
        ) : (
          <>
            <Link href="/login">
              <span className="hover:underline">Login</span>
            </Link>
            <Link href="/register">
              <span className="hover:underline">Register</span>
            </Link>
          </>
        )}
        <ThemeToggle />
      </div>
    </nav>
  );
}
