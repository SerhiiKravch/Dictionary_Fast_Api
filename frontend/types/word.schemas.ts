import { z } from "zod";

export const languageCodeSchema = z.enum(["en", "uk"]);

export const lookupDirectionSchema = z.enum(["en:uk", "uk:en"]);

export const wordOriginSchema = z.enum(["manual", "openai", "imported"]);

export const partOfSpeechSchema = z.enum([
  "noun",
  "verb",
  "adjective",
  "adverb",
  "pronoun",
  "preposition",
  "conjunction",
  "interjection",
  "phrase",
  "other",
]);

export const translationOptionReadSchema = z.object({
  id: z.number().int(),
  text: z.string(),
  part_of_speech: partOfSpeechSchema,
  priority: z.number().int(),
  usage_note: z.string(),
});

export const translationOptionCreateSchema = z.object({
  text: z.string().min(1),
  part_of_speech: partOfSpeechSchema.optional(),
  priority: z.number().int().min(1).optional(),
  usage_note: z.string().optional(),
});

export const wordReadSchema = z.object({
  id: z.number().int(),
  source_word: z.string(),
  source_language: languageCodeSchema,
  target_language: languageCodeSchema,
  slug: z.string(),
  transcription: z.string(),
  primary_translation: z.string(),
  context_sentence: z.string(),
  origin: wordOriginSchema,
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
  translation_options: z.array(translationOptionReadSchema),
});

export const wordCreateSchema = z.object({
  source_word: z.string().min(1),
  source_language: languageCodeSchema,
  target_language: languageCodeSchema,
  transcription: z.string().min(1),
  primary_translation: z.string().min(1),
  context_sentence: z.string().min(1),
  origin: wordOriginSchema.optional(),
  translation_options: z.array(translationOptionCreateSchema).optional(),
});

export const wordLookupRequestSchema = z.object({
  word: z.string().min(1),
  direction: lookupDirectionSchema,
});

export const wordListResponseSchema = z.object({
  items: z.array(wordReadSchema),
  total: z.number().int().nonnegative(),
  limit: z.number().int().positive(),
  offset: z.number().int().nonnegative(),
});

export const autocompleteResponseSchema = z.object({
  results: z.array(z.string()),
});

export const backendValidationErrorSchema = z.object({
  type: z.string(),
  loc: z.array(z.union([z.string(), z.number()])),
  msg: z.string(),
  input: z.unknown().optional(),
});

export const errorResponseSchema = z.object({
  detail: z.string(),
  error_code: z.string(),
  errors: z.array(backendValidationErrorSchema),
});
