"use client";

import Link from "next/link";

import { Button, buttonClassName } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type GlobalErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <Card className="stack-md">
          <div className="section-heading">
            <p className="eyebrow">Application error</p>
            <h1>We could not render this part of the dictionary app.</h1>
            <p>
              Something failed outside the route-specific fallbacks. Retry the current screen or
              move to one of the stable entry points below.
            </p>
          </div>

          <div className="message message--error">
            <strong>Error details:</strong> {error.message || "Unknown application error."}
          </div>

          <div className="actions-row">
            <Button variant="primary" type="button" onClick={() => reset()}>
              Try again
            </Button>
            <Link className={buttonClassName()} href="/">
              Back to search
            </Link>
            <Link className={buttonClassName()} href="/words">
              Open catalog
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
