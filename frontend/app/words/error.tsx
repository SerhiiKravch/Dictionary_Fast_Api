"use client";

import Link from "next/link";

type WordsErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function WordsError({ error, reset }: WordsErrorProps) {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <div className="panel stack-md">
          <div className="section-heading">
            <p className="eyebrow">Dictionary error</p>
            <h1>We could not load this dictionary view.</h1>
            <p>
              The backend or the current route data failed to load. You can retry this segment or
              move back to a stable page.
            </p>
          </div>

          <div className="message message--error">
            <strong>Error details:</strong> {error.message || "Unknown route error."}
          </div>

          <div className="actions-row">
            <button className="button button--primary" type="button" onClick={() => reset()}>
              Try again
            </button>
            <Link className="button" href="/words">
              Back to catalog
            </Link>
            <Link className="button" href="/">
              Back to search
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
