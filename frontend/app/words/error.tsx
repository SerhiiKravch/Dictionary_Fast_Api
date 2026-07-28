"use client";

import Link from "next/link";

import { Button, buttonClassName } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type WordsErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function WordsError({ error, reset }: WordsErrorProps) {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <Card className="stack-md">
          <div className="section-heading">
            <p className="eyebrow">Catalog error</p>
            <h1>We could not load the dictionary catalog.</h1>
            <p>
              The list request, filters, or paginated catalog data failed to load. Retry the
              current view or jump back to another stable route.
            </p>
          </div>

          <div className="message message--error">
            <strong>Error details:</strong> {error.message || "Unknown route error."}
          </div>

          <div className="actions-row">
            <Button variant="primary" type="button" onClick={() => reset()}>
              Try again
            </Button>
            <Link className={buttonClassName()} href="/words/new">
              Add word manually
            </Link>
            <Link className={buttonClassName()} href="/words">
              Back to catalog
            </Link>
            <Link className={buttonClassName()} href="/">
              Back to search
            </Link>
          </div>
        </Card>
      </section>
    </main>
  );
}
