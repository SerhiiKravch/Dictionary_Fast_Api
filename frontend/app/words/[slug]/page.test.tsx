import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiClientError } from "@/services/api-client";

import WordDetailsPage, { generateMetadata } from "./page";

const getWordBySlugMock = vi.hoisted(() => vi.fn());
const notFoundMock = vi.hoisted(() => vi.fn(() => {
  throw new Error("NEXT_NOT_FOUND");
}));

vi.mock("@/services/words", () => ({
  getWordBySlug: getWordBySlugMock,
}));

vi.mock("next/navigation", () => ({
  notFound: notFoundMock,
}));

describe("app/words/[slug]/page", () => {
  beforeEach(() => {
    getWordBySlugMock.mockReset();
    notFoundMock.mockClear();
  });

  it("renders the word details page", async () => {
    getWordBySlugMock.mockResolvedValue({
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
    });

    const page = await WordDetailsPage({
      params: Promise.resolve({ slug: "apple-en-uk" }),
    });

    render(page);

    expect(getWordBySlugMock).toHaveBeenCalledWith("apple-en-uk");
    expect(screen.getByRole("heading", { name: "apple" })).toBeVisible();
    expect(screen.getByText("яблуко")).toBeVisible();
    expect(screen.getByText("Only the primary translation is available.")).toBeVisible();
  });

  it("delegates missing slugs to notFound()", async () => {
    getWordBySlugMock.mockRejectedValue(
      new ApiClientError({
        message: "Word not found.",
        status: 404,
        errorCode: "word_not_found",
        details: null,
      }),
    );

    await expect(
      WordDetailsPage({
        params: Promise.resolve({ slug: "missing-slug" }),
      }),
    ).rejects.toThrow("NEXT_NOT_FOUND");

    expect(notFoundMock).toHaveBeenCalled();
  });
});

describe("generateMetadata", () => {
  beforeEach(() => {
    getWordBySlugMock.mockReset();
  });

  it("builds metadata from the returned word", async () => {
    getWordBySlugMock.mockResolvedValue({
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
    });

    await expect(
      generateMetadata({
        params: Promise.resolve({ slug: "apple-en-uk" }),
      }),
    ).resolves.toEqual({
      title: "apple — яблуко | Dictionary",
      description: "Translation, transcription and usage example for apple.",
    });
  });

  it("returns not-found metadata when the slug is missing", async () => {
    getWordBySlugMock.mockRejectedValue(
      new ApiClientError({
        message: "Word not found.",
        status: 404,
        errorCode: "word_not_found",
        details: null,
      }),
    );

    await expect(
      generateMetadata({
        params: Promise.resolve({ slug: "missing-slug" }),
      }),
    ).resolves.toEqual({
      title: "Word not found | Dictionary",
      description: "The requested dictionary entry could not be found.",
    });
  });
});
