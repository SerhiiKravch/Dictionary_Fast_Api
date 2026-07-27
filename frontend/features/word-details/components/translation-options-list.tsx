import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { StatePanel } from "@/components/ui/state-panel";
import type { TranslationOptionRead } from "@/types/word";

type TranslationOptionsListProps = {
  options: TranslationOptionRead[];
};

export function TranslationOptionsList({ options }: TranslationOptionsListProps) {
  return (
    <Card as="section" className="stack-md">
      <div className="section-heading section-heading--compact">
        <h2>Translation options</h2>
        <p>Alternative meanings, parts of speech, and notes returned by the backend.</p>
      </div>

      {options.length === 0 ? (
        <StatePanel
          eyebrow="No alternatives yet"
          title="Only the primary translation is available."
          description="Additional meanings, usage notes, and part-of-speech hints have not been saved for this word yet."
        />
      ) : (
        <div className="stack-sm">
          {options.map((option) => (
            <article key={option.id} className="option-card">
              <div className="option-card__header">
                <strong>{option.text}</strong>
                <div className="inline-badges">
                  <Badge tone="muted">{option.part_of_speech}</Badge>
                  <Badge tone="muted">Priority {option.priority}</Badge>
                </div>
              </div>
              {option.usage_note ? (
                <p className="supporting-text">{option.usage_note}</p>
              ) : (
                <div className="empty-state empty-state--compact" aria-live="polite">
                  <span className="field-label">Usage note</span>
                  <p className="supporting-text">
                    No extra note was added for this translation option.
                  </p>
                </div>
              )}
            </article>
          ))}
        </div>
      )}
    </Card>
  );
}
