export type LanguageCode = "en" | "uk";

export type LookupDirection = "en:uk" | "uk:en";

export type WordOrigin = "manual" | "openai" | "imported";

export type PartOfSpeech =
  | "noun"
  | "verb"
  | "adjective"
  | "adverb"
  | "pronoun"
  | "preposition"
  | "conjunction"
  | "interjection"
  | "phrase"
  | "other";

export type TranslationOptionRead = {
  id: number;
  text: string;
  part_of_speech: PartOfSpeech;
  priority: number;
  usage_note: string;
};

export type TranslationOptionCreate = {
  text: string;
  part_of_speech?: PartOfSpeech;
  priority?: number;
  usage_note?: string;
};

export type WordRead = {
  id: number;
  source_word: string;
  source_language: LanguageCode;
  target_language: LanguageCode;
  slug: string;
  transcription: string;
  primary_translation: string;
  context_sentence: string;
  origin: WordOrigin;
  created_at: string;
  updated_at: string;
  translation_options: TranslationOptionRead[];
};

export type WordCreate = {
  source_word: string;
  source_language: LanguageCode;
  target_language: LanguageCode;
  transcription: string;
  primary_translation: string;
  context_sentence: string;
  origin?: WordOrigin;
  translation_options?: TranslationOptionCreate[];
};

export type WordLookupRequest = {
  word: string;
  direction: LookupDirection;
};

export type WordListResponse = {
  items: WordRead[];
  total: number;
  limit: number;
  offset: number;
};

export type AutocompleteResponse = {
  results: string[];
};

export type BackendValidationError = {
  type: string;
  loc: Array<string | number>;
  msg: string;
  input?: unknown;
};

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

export type ErrorResponse = {
  detail: string;
  error_code: ErrorCode | string;
  errors: BackendValidationError[];
};

export type WordsQueryParams = {
  limit?: number;
  offset?: number;
  source_language?: LanguageCode;
  target_language?: LanguageCode;
  origin?: WordOrigin;
  search?: string;
};
