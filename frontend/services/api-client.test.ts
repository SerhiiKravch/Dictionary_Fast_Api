import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiClientError, normalizeApiError, request } from "./api-client";

describe("request", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("builds the request URL, skips empty query values, and sends JSON body", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    vi.stubGlobal("fetch", fetchMock);

    const result = await request<{ ok: boolean }>("/api/words", {
      method: "POST",
      body: { source_word: "hello" },
      query: {
        limit: 20,
        search: "hi",
        origin: "",
        offset: undefined,
      },
    });

    expect(result).toEqual({ ok: true });
    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/api/words?limit=20&search=hi",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ source_word: "hello" }),
        cache: "no-store",
        headers: expect.objectContaining({
          "Content-Type": "application/json",
        }),
      }),
    );
  });

  it("throws ApiClientError with backend payload details", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            detail: "This word already exists.",
            error_code: "word_already_exists",
            errors: [],
          }),
          {
            status: 409,
            headers: { "Content-Type": "application/json" },
          },
        ),
      ),
    );

    await expect(request("/api/words")).rejects.toMatchObject({
      name: "ApiClientError",
      message: "This word already exists.",
      status: 409,
      errorCode: "word_already_exists",
    });
  });

  it("throws when the response payload is not JSON", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("not-json", {
          status: 200,
          headers: { "Content-Type": "text/plain" },
        }),
      ),
    );

    await expect(request("/api/words")).rejects.toMatchObject({
      name: "ApiClientError",
      message: "Expected a JSON response but received a different payload.",
      status: 200,
      errorCode: "unknown_error",
    });
  });
});

describe("normalizeApiError", () => {
  it("falls back to known messages when backend detail is missing", () => {
    const error = normalizeApiError(503, {
      detail: "",
      error_code: "database_connection_error",
      errors: [],
    });

    expect(error).toBeInstanceOf(ApiClientError);
    expect(error.message).toBe("Database is temporarily unavailable.");
    expect(error.status).toBe(503);
  });
});
