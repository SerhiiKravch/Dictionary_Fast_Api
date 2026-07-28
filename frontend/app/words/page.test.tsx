import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiClientError } from "@/services/api-client";

import WordsPage from "./page";

const getWordsMock = vi.hoisted(() => vi.fn());
const pushMock = vi.hoisted(() => vi.fn());

vi.mock("@/services/words", () => ({
  getWords: getWordsMock,
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: pushMock,
  }),
  usePathname: () => "/words",
  useSearchParams: () => new URLSearchParams("search=apple&limit=20&offset=0"),
  notFound: vi.fn(),
}));

describe("app/words/page", () => {
  beforeEach(() => {
    getWordsMock.mockReset();
    pushMock.mockReset();
  });

  it("loads and renders the catalog using normalized search params", async () => {
    getWordsMock.mockResolvedValue({
      items: [
        {
          id: 1,
          source_word: "apple",
          source_language: "en",
          target_language: "uk",
          slug: "apple-en-uk",
          transcription: "[ap-l]",
          primary_translation: "яблуко",
          context_sentence: "I ate an apple.",
          origin: "manual",
          created_at: "2026-07-20T12:00:00.000Z",
          updated_at: "2026-07-21T12:00:00.000Z",
          translation_options: [],
        },
      ],
      total: 1,
      limit: 20,
      offset: 0,
    });

    const page = await WordsPage({
      searchParams: Promise.resolve({
        search: "  apple  ",
        source_language: "en",
        target_language: "uk",
        origin: "manual",
        limit: "20",
        offset: "0",
      }),
    });

    render(page);

    expect(getWordsMock).toHaveBeenCalledWith({
      search: "apple",
      source_language: "en",
      target_language: "uk",
      origin: "manual",
      limit: 20,
      offset: 0,
    });
    expect(screen.getByRole("heading", { name: "Browse saved words" })).toBeVisible();
    expect(screen.getByText("1 words found")).toBeVisible();
    expect(screen.getByText("apple")).toBeVisible();
  });

  it("renders a route-level fallback when catalog loading fails", async () => {
    getWordsMock.mockRejectedValue(
      new ApiClientError({
        message: "Database is temporarily unavailable.",
        status: 503,
        errorCode: "database_connection_error",
        details: null,
      }),
    );

    const page = await WordsPage({
      searchParams: Promise.resolve({
        search: "apple",
      }),
    });

    render(page);

    expect(screen.getByText("Catalog unavailable")).toBeVisible();
    expect(screen.getByText("We could not load this slice of the dictionary.")).toBeVisible();
    expect(screen.getByText("Database is temporarily unavailable.")).toBeVisible();
  });
});
