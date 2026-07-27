import { beforeEach, describe, expect, it, vi } from "vitest";

import type { WordCreate, WordsQueryParams } from "@/types/word";

import {
  createWord,
  getAutocomplete,
  getWordBySlug,
  getWords,
  lookupWord,
} from "./words";

const requestMock = vi.hoisted(() => vi.fn());

vi.mock("@/services/api-client", () => ({
  request: requestMock,
}));

describe("words service", () => {
  beforeEach(() => {
    requestMock.mockReset();
  });

  it("delegates lookupWord to the request helper", async () => {
    requestMock.mockResolvedValue({ slug: "hello" });

    await lookupWord({ word: "hello", direction: "en:uk" });

    expect(requestMock).toHaveBeenCalledWith("/lookup", {
      method: "POST",
      body: { word: "hello", direction: "en:uk" },
    });
  });

  it("passes query params to getWords", async () => {
    const params: WordsQueryParams = { limit: 10, offset: 20, search: "pho" };

    requestMock.mockResolvedValue({ items: [], total: 0, limit: 10, offset: 20 });

    await getWords(params);

    expect(requestMock).toHaveBeenCalledWith("/api/words", {
      query: params,
    });
  });

  it("uses the correct endpoints for detail, create, and autocomplete actions", async () => {
    const payload: WordCreate = {
      source_word: "hello",
      source_language: "en",
      target_language: "uk",
      transcription: "[həˈləʊ]",
      primary_translation: "привіт",
      context_sentence: "Hello there",
      translation_options: [],
    };

    requestMock.mockResolvedValue({});

    await getWordBySlug("hello");
    await createWord(payload);
    await getAutocomplete("hel");

    expect(requestMock).toHaveBeenNthCalledWith(1, "/api/words/hello");
    expect(requestMock).toHaveBeenNthCalledWith(2, "/api/words", {
      method: "POST",
      body: payload,
    });
    expect(requestMock).toHaveBeenNthCalledWith(3, "/api/autocomplete", {
      query: { q: "hel" },
    });
  });
});
