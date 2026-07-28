"use client";

import Link from "next/link";

import { Button, buttonClassName } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type CreateWordErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function CreateWordError({ error, reset }: CreateWordErrorProps) {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <Card className="stack-md">
          <div className="section-heading">
            <p className="eyebrow">Creation error</p>
            <h1>We could not open the manual creation workspace.</h1>
            <p>
              The form shell or its required route data failed to load. You can retry this route
              or fall back to search and catalog flows.
            </p>
          </div>

          <div className="message message--error">
            <strong>Error details:</strong> {error.message || "Unknown route error."}
          </div>

          <div className="actions-row">
            <Button variant="primary" type="button" onClick={() => reset()}>
              Retry form
            </Button>
            <Link className={buttonClassName()} href="/">
              Back to search
            </Link>
            <Link className={buttonClassName()} href="/words">
              Open catalog
            </Link>
          </div>
        </Card>
      </section>
    </main>
  );
}
