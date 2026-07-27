import { Card } from "@/components/ui/card";

export default function CreateWordLoading() {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <div className="section-heading">
          <p className="eyebrow">Manual creation</p>
          <h1>Preparing form...</h1>
          <p>Loading the word creation workspace.</p>
        </div>

        <Card className="stack-md">
          <div className="form-grid">
            {Array.from({ length: 6 }).map((_, index) => (
              <div key={index} className="stack-sm">
                <div className="skeleton skeleton-label" />
                <div className="skeleton skeleton-input" />
              </div>
            ))}
          </div>

          <div className="stack-sm">
            <div className="skeleton skeleton-label" />
            <div className="skeleton skeleton-textarea" />
          </div>

          <div className="option-editor">
            <div className="form-grid">
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
          </div>

          <div className="skeleton skeleton-button" />
        </Card>
      </section>
    </main>
  );
}
