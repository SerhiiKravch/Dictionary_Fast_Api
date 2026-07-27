export default function WordsLoading() {
  return (
    <main className="page-shell">
      <section className="page-section">
        <div className="section-heading">
          <p className="eyebrow">Dictionary catalog</p>
          <h1>Loading words...</h1>
          <p>Fetching dictionary entries, filters, and pagination.</p>
        </div>

        <div className="panel filters-grid">
          <div className="stack-sm">
            <div className="skeleton skeleton-label" />
            <div className="skeleton skeleton-input" />
          </div>
          <div className="stack-sm">
            <div className="skeleton skeleton-label" />
            <div className="skeleton skeleton-input" />
          </div>
          <div className="stack-sm">
            <div className="skeleton skeleton-label" />
            <div className="skeleton skeleton-input" />
          </div>
          <div className="stack-sm">
            <div className="skeleton skeleton-label" />
            <div className="skeleton skeleton-input" />
          </div>
        </div>

        <div className="stack-md">
          {Array.from({ length: 4 }).map((_, index) => (
            <article key={index} className="catalog-card">
              <div className="inline-badges">
                <div className="skeleton skeleton-badge" />
                <div className="skeleton skeleton-badge" />
                <div className="skeleton skeleton-badge" />
              </div>
              <div className="stack-sm">
                <div className="skeleton skeleton-title" />
                <div className="skeleton skeleton-text" />
                <div className="skeleton skeleton-text skeleton-text--wide" />
              </div>
            </article>
          ))}
        </div>

        <div className="pagination">
          <div className="skeleton skeleton-button" />
          <div className="skeleton skeleton-text" />
          <div className="skeleton skeleton-button" />
        </div>
      </section>
    </main>
  );
}
