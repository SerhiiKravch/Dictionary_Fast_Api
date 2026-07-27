import type { WordRead } from "@/types/word";

type WordDetailsCardProps = {
  word: WordRead;
};

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(value));
}

export function WordDetailsCard({ word }: WordDetailsCardProps) {
  return (
    <article className="panel stack-md">
      <div className="stack-sm">
        <div className="inline-badges">
          <span className="badge">{word.source_language.toUpperCase()}</span>
          <span className="badge">{word.target_language.toUpperCase()}</span>
          <span className="badge badge--muted">{word.origin}</span>
        </div>
        <h1 className="hero-title">{word.source_word}</h1>
        <p className="supporting-text">{word.transcription}</p>
      </div>

      <div className="definition-card">
        <span className="field-label">Primary translation</span>
        <p className="definition-card__value">{word.primary_translation}</p>
      </div>

      <div className="stack-sm">
        <span className="field-label">Context sentence</span>
        <p className="supporting-text">{word.context_sentence}</p>
      </div>

      <dl className="metadata-grid">
        <div>
          <dt>Created</dt>
          <dd>{formatDate(word.created_at)}</dd>
        </div>
        <div>
          <dt>Updated</dt>
          <dd>{formatDate(word.updated_at)}</dd>
        </div>
      </dl>
    </article>
  );
}
