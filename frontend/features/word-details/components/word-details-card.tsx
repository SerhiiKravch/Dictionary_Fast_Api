import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
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
    <Card as="article" className="stack-md">
      <div className="stack-sm">
        <div className="inline-badges">
          <Badge>{word.source_language.toUpperCase()}</Badge>
          <Badge>{word.target_language.toUpperCase()}</Badge>
          <Badge tone="muted">{word.origin}</Badge>
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
    </Card>
  );
}
