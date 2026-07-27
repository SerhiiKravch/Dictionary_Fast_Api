import { Card } from "@/components/ui/card";
import { DictionarySearchForm } from "@/features/dictionary-search/components/dictionary-search-form";

export default function HomePage() {
  return (
    <main className="page-shell">
      <section className="hero-grid">
        <Card className="status-card">
          <p className="eyebrow">Search-first dictionary</p>
          <h1>Look up words across English and Ukrainian.</h1>
          <p>
            This frontend now includes the first route map, a reusable API layer, and the
            interactive search flow on top of your FastAPI backend.
          </p>
        </Card>

        <div>
          <DictionarySearchForm />
        </div>
      </section>

      <section className="page-section page-section--compact">
        <div className="card-grid">
          <Card as="article" className="stack-sm">
            <span className="field-label">Catalog</span>
            <h2>Browse saved words</h2>
            <p className="supporting-text">
              Use URL-driven filters and pagination on the catalog screen.
            </p>
          </Card>

          <Card as="article" className="stack-sm">
            <span className="field-label">Details</span>
            <h2>Read full word cards</h2>
            <p className="supporting-text">
              Each word gets its own server-rendered detail page with translation options.
            </p>
          </Card>

          <Card as="article" className="stack-sm">
            <span className="field-label">Manual entry</span>
            <h2>Create missing words</h2>
            <p className="supporting-text">
              Add a new dictionary entry manually and redirect straight to its detail page.
            </p>
          </Card>
        </div>
      </section>
    </main>
  );
}
