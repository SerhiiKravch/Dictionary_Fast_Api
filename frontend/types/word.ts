import type { z } from "zod";

import type {
  autocompleteResponseSchema,
  backendValidationErrorSchema,
  errorResponseSchema,
  languageCodeSchema,
  lookupDirectionSchema,
  partOfSpeechSchema,
  translationOptionCreateSchema,
  translationOptionReadSchema,
  wordCreateSchema,
  wordListResponseSchema,
  wordLookupRequestSchema,
  wordOriginSchema,
  wordReadSchema,
} from "./word.schemas";

export type LanguageCode = z.infer<typeof languageCodeSchema>;

export type LookupDirection = z.infer<typeof lookupDirectionSchema>;

export type WordOrigin = z.infer<typeof wordOriginSchema>;

export type PartOfSpeech = z.infer<typeof partOfSpeechSchema>;

export type TranslationOptionRead = z.infer<typeof translationOptionReadSchema>;

export type TranslationOptionCreate = z.infer<typeof translationOptionCreateSchema>;

export type WordRead = z.infer<typeof wordReadSchema>;

export type WordCreate = z.infer<typeof wordCreateSchema>;

export type WordLookupRequest = z.infer<typeof wordLookupRequestSchema>;

export type WordListResponse = z.infer<typeof wordListResponseSchema>;

export type AutocompleteResponse = z.infer<typeof autocompleteResponseSchema>;

export type BackendValidationError = z.infer<typeof backendValidationErrorSchema>;

export type ErrorCode =
  | "application_error"
  | "database_connection_error"
  | "integration_error"
  | "openai_configuration_error"
  | "openai_rate_limit"
  | "openai_response_format_error"
  | "openai_unavailable"
  | "persistence_error"
  | "request_validation_error"
  | "validation_error"
  | "word_already_exists"
  | "word_not_found"
  | "unknown_error";

export type ErrorResponse = z.infer<typeof errorResponseSchema>;

export type WordsQueryParams = {
  limit?: number;
  offset?: number;
  source_language?: LanguageCode;
  target_language?: LanguageCode;
  origin?: WordOrigin;
  search?: string;
};
