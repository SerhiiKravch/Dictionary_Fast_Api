"use client";

import Link from "next/link";

import { Button, buttonClassName } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type WordDetailsErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function WordDetailsError({ error, reset }: WordDetailsErrorProps) {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <Card className="stack-md">
          <div className="section-heading">
            <p className="eyebrow">Detail error</p>
            <h1>We could not load this dictionary entry.</h1>
            <p>
              The word details, metadata, or related translation content failed to render. Retry
              this slug or return to a stable route.
            </p>
          </div>

          <div className="message message--error">
            <strong>Error details:</strong> {error.message || "Unknown detail route error."}
          </div>

          <div className="actions-row">
            <Button variant="primary" type="button" onClick={() => reset()}>
              Retry entry
            </Button>
            <Link className={buttonClassName()} href="/words">
              Back to catalog
            </Link>
            <Link className={buttonClassName()} href="/">
              Back to search
            </Link>
            <Link className={buttonClassName()} href="/words/new">
              Add word manually
            </Link>
          </div>
        </Card>
      </section>
    </main>
  );
}
