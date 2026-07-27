import { request } from "@/services/api-client";
import type {
  AutocompleteResponse,
  WordCreate,
  WordListResponse,
  WordLookupRequest,
  WordRead,
  WordsQueryParams,
} from "@/types/word";

export function lookupWord(payload: WordLookupRequest) {
  return request<WordRead>("/lookup", {
    method: "POST",
    body: payload,
  });
}

export function getWords(params: WordsQueryParams = {}) {
  return request<WordListResponse>("/api/words", {
    query: params,
  });
}

export function getWordBySlug(slug: string) {
  return request<WordRead>(`/api/words/${slug}`);
}

export function createWord(payload: WordCreate) {
  return request<WordRead>("/api/words", {
    method: "POST",
    body: payload,
  });
}

export function getAutocomplete(query: string) {
  return request<AutocompleteResponse>("/api/autocomplete", {
    query: { q: query },
  });
}
