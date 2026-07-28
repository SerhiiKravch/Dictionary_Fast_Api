import { Card } from "@/components/ui/card";

export default function WordDetailsLoading() {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <Card as="article" className="stack-md">
          <div className="inline-badges">
            <div className="skeleton skeleton-badge" />
            <div className="skeleton skeleton-badge" />
            <div className="skeleton skeleton-badge" />
          </div>

          <div className="skeleton skeleton-hero" />
          <div className="skeleton skeleton-text" />

          <div className="definition-card stack-sm">
            <div className="skeleton skeleton-label" />
            <div className="skeleton skeleton-title" />
          </div>

          <div className="stack-sm">
            <div className="skeleton skeleton-label" />
            <div className="skeleton skeleton-text skeleton-text--wide" />
            <div className="skeleton skeleton-text skeleton-text--wide" />
          </div>
        </Card>

        <Card as="section" className="stack-md">
          <div className="section-heading section-heading--compact">
            <h2>Loading translation options...</h2>
            <p>Preparing detailed word data.</p>
          </div>

          <div className="stack-sm">
            {Array.from({ length: 3 }).map((_, index) => (
              <article key={index} className="option-card">
                <div className="option-card__header">
                  <div className="skeleton skeleton-text" />
                  <div className="inline-badges">
                    <div className="skeleton skeleton-badge" />
                    <div className="skeleton skeleton-badge" />
                  </div>
                </div>
                <div className="skeleton skeleton-text skeleton-text--wide" />
              </article>
            ))}
          </div>
        </Card>
      </section>
    </main>
  );
}
