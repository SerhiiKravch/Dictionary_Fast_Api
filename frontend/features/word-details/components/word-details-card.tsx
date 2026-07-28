import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { StatePanel } from "@/components/ui/state-panel";
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
  const hasTranscription = Boolean(word.transcription?.trim());
  const hasContextSentence = Boolean(word.context_sentence?.trim());
  const hasCreatedAt = Boolean(word.created_at);
  const hasUpdatedAt = Boolean(word.updated_at);
  const hasMetadata = hasCreatedAt || hasUpdatedAt;

  return (
    <Card as="article" className="stack-md">
      <div className="stack-sm">
        <div className="inline-badges">
          <Badge>{word.source_language.toUpperCase()}</Badge>
          <Badge>{word.target_language.toUpperCase()}</Badge>
          <Badge tone="muted">{word.origin}</Badge>
        </div>
        <h1 className="hero-title">{word.source_word}</h1>
        {hasTranscription ? (
          <p className="supporting-text">{word.transcription}</p>
        ) : (
          <div className="empty-state empty-state--compact" aria-live="polite">
            <span className="field-label">Transcription</span>
            <p className="supporting-text">
              No pronunciation note has been saved for this word yet.
            </p>
          </div>
        )}
      </div>

      <div className="definition-card">
        <span className="field-label">Primary translation</span>
        <p className="definition-card__value">{word.primary_translation}</p>
      </div>

      {hasContextSentence ? (
        <div className="stack-sm">
          <span className="field-label">Context sentence</span>
          <p className="supporting-text">{word.context_sentence}</p>
        </div>
      ) : (
        <StatePanel
          eyebrow="No example yet"
          title="This word does not have a saved usage example."
          description="Add a context sentence later to make the entry easier to remember in real use."
        />
      )}

      {hasMetadata ? (
        <dl className="metadata-grid">
          <div>
            <dt>Created</dt>
            <dd>{hasCreatedAt ? formatDate(word.created_at) : "Not available"}</dd>
          </div>
          <div>
            <dt>Updated</dt>
            <dd>{hasUpdatedAt ? formatDate(word.updated_at) : "Not available"}</dd>
          </div>
        </dl>
      ) : (
        <div className="empty-state empty-state--compact" aria-live="polite">
          <span className="field-label">Metadata</span>
          <p className="supporting-text">
            Timestamps are not available for this dictionary entry yet.
          </p>
        </div>
      )}
    </Card>
  );
}
