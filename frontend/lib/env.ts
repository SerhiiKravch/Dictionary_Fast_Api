const publicApiUrl = process.env.NEXT_PUBLIC_API_URL?.trim();
const internalApiUrl = process.env.INTERNAL_API_URL?.trim();

export function getApiBaseUrl() {
  if (typeof window === "undefined") {
    return internalApiUrl || publicApiUrl || "http://127.0.0.1:8000";
  }

  return publicApiUrl || "http://127.0.0.1:8000";
}
