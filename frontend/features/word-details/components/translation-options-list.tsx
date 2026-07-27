import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
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
        <p className="supporting-text">No additional translation options available yet.</p>
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
              {option.usage_note ? <p className="supporting-text">{option.usage_note}</p> : null}
            </article>
          ))}
        </div>
      )}
    </Card>
  );
}
