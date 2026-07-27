import Link from "next/link";

import type { WordRead } from "@/types/word";

type WordsListProps = {
  words: WordRead[];
};

export function WordsList({ words }: WordsListProps) {
  if (words.length === 0) {
    return (
      <div className="empty-state">
        <h2>No words found</h2>
        <p>Adjust filters, try another search term, or add a word manually.</p>
      </div>
    );
  }

  return (
    <div className="stack-md">
      {words.map((word) => (
        <article key={word.id} className="catalog-card">
          <div className="catalog-card__meta">
            <span className="badge">{word.source_language.toUpperCase()}</span>
            <span className="badge">{word.target_language.toUpperCase()}</span>
            <span className="badge badge--muted">{word.origin}</span>
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
