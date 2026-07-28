import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { buttonClassName } from "@/components/ui/button";
import { StatePanel } from "@/components/ui/state-panel";
import type { WordRead } from "@/types/word";

type WordsListProps = {
  words: WordRead[];
  hasActiveFilters?: boolean;
};

export function WordsList({ words, hasActiveFilters = false }: WordsListProps) {
  if (words.length === 0) {
    return (
      <StatePanel
        aria-live="polite"
        eyebrow={hasActiveFilters ? "No matches" : "Empty catalog"}
        title={hasActiveFilters ? "No words matched these filters." : "Your dictionary is still empty."}
        description={
          hasActiveFilters
            ? "Try another search term or relax the filters to see more saved words."
            : "Add the first word manually or use the search flow to start building the catalog."
        }
        actions={
          <>
            <Link className={buttonClassName("primary")} href="/words/new">
              Add a word
            </Link>
            {hasActiveFilters ? (
              <Link className={buttonClassName()} href="/words">
                Clear filters
              </Link>
            ) : (
              <Link className={buttonClassName()} href="/">
                Open search
              </Link>
            )}
          </>
        }
      />
    );
  }

  return (
    <div className="stack-md">
      {words.map((word) => (
        <article key={word.id} className="catalog-card">
          <div className="catalog-card__meta">
            <Badge>{word.source_language.toUpperCase()}</Badge>
            <Badge>{word.target_language.toUpperCase()}</Badge>
            <Badge tone="muted">{word.origin}</Badge>
          </div>

          <div className="catalog-card__content">
            <div>
              <h2>
                <Link href={`/words/${word.slug}`}>{word.source_word}</Link>
              </h2>
              <p className="catalog-card__transcription">{word.transcription}</p>
            </div>

            <div>
              <p className="catalog-card__translation">{word.primary_translation}</p>
              <p className="catalog-card__context">{word.context_sentence}</p>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
