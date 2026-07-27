import { CreateWordForm } from "@/features/word-form/components/create-word-form";

export default function CreateWordPage() {
  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <div className="section-heading">
          <p className="eyebrow">Manual creation</p>
          <h1>Add a new dictionary entry</h1>
          <p>
            Use the backend validation rules, then redirect to the saved word page after a
            successful create.
          </p>
        </div>

        <CreateWordForm />
      </section>
    </main>
  );
}
