import Link from "next/link";

import { buttonClassName } from "@/components/ui/button";
import { StatePanel } from "@/components/ui/state-panel";
import { ApiClientError } from "@/services/api-client";
import { getWords } from "@/services/words";
import type { LanguageCode, WordOrigin, WordsQueryParams } from "@/types/word";
import { Pagination } from "@/features/words-list/components/pagination";
import { WordsFilters } from "@/features/words-list/components/words-filters";
import { WordsList } from "@/features/words-list/components/words-list";

type SearchParams = Record<string, string | string[] | undefined>;
type WordsPageDataResult =
  | { ok: true; words: Awaited<ReturnType<typeof getWords>> }
  | { ok: false; description: string };

type WordsPageProps = {
  searchParams?: Promise<SearchParams>;
};

function readFirst(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

function parsePositiveInt(value: string | undefined, fallback: number) {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function parseNonNegativeInt(value: string | undefined, fallback: number) {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : fallback;
}

function isLanguageCode(value: string | undefined): value is LanguageCode {
  return value === "en" || value === "uk";
}

function isWordOrigin(value: string | undefined): value is WordOrigin {
  return value === "manual" || value === "openai" || value === "imported";
}

function parseWordsQueryParams(searchParams: SearchParams): WordsQueryParams {
  const sourceLanguage = readFirst(searchParams.source_language);
  const targetLanguage = readFirst(searchParams.target_language);
  const origin = readFirst(searchParams.origin);
  const search = readFirst(searchParams.search)?.trim() ?? "";

  return {
    limit: parsePositiveInt(readFirst(searchParams.limit), 20),
    offset: parseNonNegativeInt(readFirst(searchParams.offset), 0),
    source_language: isLanguageCode(sourceLanguage) ? sourceLanguage : undefined,
    target_language: isLanguageCode(targetLanguage) ? targetLanguage : undefined,
    origin: isWordOrigin(origin) ? origin : undefined,
    search: search || undefined,
  };
}

async function loadWords(filters: WordsQueryParams): Promise<WordsPageDataResult> {
  try {
    const words = await getWords(filters);
    return { ok: true, words };
  } catch (error) {
    return {
      ok: false,
      description:
        error instanceof ApiClientError
          ? error.message
          : "The catalog request did not complete. Please try again in a moment.",
    };
  }
}

export default async function WordsPage({ searchParams }: WordsPageProps) {
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const filters = parseWordsQueryParams(resolvedSearchParams);
  const hasActiveFilters = Boolean(
    filters.search || filters.source_language || filters.target_language || filters.origin,
  );
  const result = await loadWords(filters);

  return (
    <main className="page-shell">
      <section className="page-section">
        <div className="section-heading">
          <p className="eyebrow">Dictionary catalog</p>
          <h1>Browse saved words</h1>
          <p>
            Filter by direction, origin, and search term while keeping the URL as the source of
            truth.
          </p>
        </div>

        <WordsFilters filters={filters} />

        {result.ok ? (
          <>
            <div className="catalog-meta" aria-live="polite">
              <span>{result.words.total} words found</span>
              <span>
                Showing {result.words.items.length === 0 ? 0 : result.words.offset + 1}-
                {Math.min(result.words.offset + result.words.limit, result.words.total)} of{" "}
                {result.words.total}
              </span>
            </div>

            <WordsList words={result.words.items} hasActiveFilters={hasActiveFilters} />
            <Pagination
              total={result.words.total}
              limit={result.words.limit}
              offset={result.words.offset}
            />
          </>
        ) : (
          <StatePanel
            tone="error"
            eyebrow="Catalog unavailable"
            title="We could not load this slice of the dictionary."
            description={result.description}
            actions={
              <>
                <Link className={buttonClassName("primary")} href="/words">
                  Reset catalog
                </Link>
                <Link className={buttonClassName()} href="/words/new">
                  Add a word manually
                </Link>
              </>
            }
          />
        )}
      </section>
    </main>
  );
}
