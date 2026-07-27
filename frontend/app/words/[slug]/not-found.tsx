import Link from "next/link";

export default function WordNotFound() {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <div className="panel stack-md">
          <div className="section-heading">
            <p className="eyebrow">Word not found</p>
            <h1>This dictionary entry does not exist.</h1>
            <p>
              The slug may be outdated, the word may have been removed, or the lookup has not been
              saved yet.
            </p>
          </div>

          <div className="actions-row">
            <Link className="button button--primary" href="/">
              Search again
            </Link>
            <Link className="button" href="/words">
              Open catalog
            </Link>
            <Link className="button" href="/words/new">
              Add word manually
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
