import { request } from "@/services/api-client";
import {
  autocompleteResponseSchema,
  wordListResponseSchema,
  wordReadSchema,
} from "@/types/word.schemas";
import type {
  WordCreate,
  WordLookupRequest,
  WordsQueryParams,
} from "@/types/word";

export function lookupWord(payload: WordLookupRequest) {
  return request("/lookup", {
    method: "POST",
    body: payload,
    schema: wordReadSchema,
  });
}

export function getWords(params: WordsQueryParams = {}) {
  return request("/api/words", {
    query: params,
    schema: wordListResponseSchema,
  });
}

export function getWordBySlug(slug: string) {
  return request(`/api/words/${slug}`, {
    schema: wordReadSchema,
  });
}

export function createWord(payload: WordCreate) {
  return request("/api/words", {
    method: "POST",
    body: payload,
    schema: wordReadSchema,
  });
}

export function getAutocomplete(query: string) {
  return request("/api/autocomplete", {
    query: { q: query },
    schema: autocompleteResponseSchema,
  });
}
