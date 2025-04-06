"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export function parseJwt(token: string): any | null {
    try {
        const payloadBase64 = token.split('.')[1];
        const payloadDecoded = window.atob(payloadBase64);
        return JSON.parse(payloadDecoded);
    } catch (error) {
        console.error("Failed to parse JWT", error);
        return null;
    }
}

export function useRedirectFromAuthPages() {
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            const payload = parseJwt(token);
            if (payload && payload.role) {
                let redirectUrl = "/dashboard/patient";
                if (payload.role === "ADMIN") {
                    redirectUrl = "/dashboard/admin";
                } else if (payload.role === "STAFF") {
                    redirectUrl = "/dashboard/staff";
                } else if (payload.role === "FINANCE") {
                    redirectUrl = "/dashboard/financial";
                }
                // Redirect and stop further execution.
                router.push(redirectUrl);
            }
        }
    }, [router]);
}

export function useEnsureDashboardAccess(expectedRole?: string[] | string) {
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            router.push("/login");
            return;
        }
        const payload = parseJwt(token);
        if (!payload || !payload.role) {
            router.push("/login");
            return;
        }
        if (expectedRole && !expectedRole.includes(payload.role)) {
            // User is logged in but trying to access the wrong dashboard.
            let redirectUrl = "/dashboard/patient";
            if (payload.role === "ADMIN") {
                redirectUrl = "/dashboard/admin";
            } else if (payload.role === "STAFF") {
                redirectUrl = "/dashboard/staff";
            } else if (payload.role === "FINANCE") {
                redirectUrl = "/dashboard/financial";
            }
            router.push(redirectUrl);
        }
    }, [router, expectedRole]);
}
