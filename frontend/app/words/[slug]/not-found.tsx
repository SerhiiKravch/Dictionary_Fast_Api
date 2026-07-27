import Link from "next/link";

import { buttonClassName } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function WordNotFound() {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <Card className="stack-md">
          <div className="section-heading">
            <p className="eyebrow">Word not found</p>
            <h1>This dictionary entry does not exist.</h1>
            <p>
              The slug may be outdated, the word may have been removed, or the lookup has not been
              saved yet.
            </p>
          </div>

          <div className="actions-row">
            <Link className={buttonClassName("primary")} href="/">
              Search again
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
