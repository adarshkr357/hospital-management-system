const API_BASE_URL: string = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function apiFetch(
    endpoint: string,
    options: RequestInit = {}
): Promise<any> {
    const token: string | null =
        typeof window !== "undefined" ? localStorage.getItem("token") : null;

    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(options.headers ? (options.headers as Record<string, string>) : {}),
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response: Response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const errorData: any = await response.json();
        throw new Error(errorData.detail || "API Error");
    }

    const data: any = await response.json();
    return data;
}

export const swrFetcher = (url: string): Promise<any> => apiFetch(url);
