import { getWords } from "@/services/words";
import type { LanguageCode, WordOrigin, WordsQueryParams } from "@/types/word";
import { Pagination } from "@/features/words-list/components/pagination";
import { WordsFilters } from "@/features/words-list/components/words-filters";
import { WordsList } from "@/features/words-list/components/words-list";

type SearchParams = Record<string, string | string[] | undefined>;

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

export default async function WordsPage({ searchParams }: WordsPageProps) {
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const filters = parseWordsQueryParams(resolvedSearchParams);
  const words = await getWords(filters);

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

        <div className="catalog-meta">
          <span>{words.total} words found</span>
          <span>
            Showing {words.items.length === 0 ? 0 : words.offset + 1}-
            {Math.min(words.offset + words.limit, words.total)} of {words.total}
          </span>
        </div>

        <WordsList words={words.items} />
        <Pagination total={words.total} limit={words.limit} offset={words.offset} />
      </section>
    </main>
  );
}
