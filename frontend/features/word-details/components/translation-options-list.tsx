import type { TranslationOptionRead } from "@/types/word";

type TranslationOptionsListProps = {
  options: TranslationOptionRead[];
};

export function TranslationOptionsList({ options }: TranslationOptionsListProps) {
  return (
    <section className="panel stack-md">
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
                  <span className="badge badge--muted">{option.part_of_speech}</span>
                  <span className="badge badge--muted">Priority {option.priority}</span>
                </div>
              </div>
              {option.usage_note ? <p className="supporting-text">{option.usage_note}</p> : null}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
