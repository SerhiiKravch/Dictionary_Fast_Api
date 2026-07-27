import { notFound } from "next/navigation";

import { TranslationOptionsList } from "@/features/word-details/components/translation-options-list";
import { WordDetailsCard } from "@/features/word-details/components/word-details-card";
import { ApiClientError } from "@/services/api-client";
import { getWordBySlug } from "@/services/words";

type WordDetailsPageProps = {
  params: Promise<{
    slug: string;
  }>;
};

export default async function WordDetailsPage({ params }: WordDetailsPageProps) {
  const { slug } = await params;
  let word;

  try {
    word = await getWordBySlug(slug);
  } catch (error) {
    if (error instanceof ApiClientError && error.errorCode === "word_not_found") {
      notFound();
    }

    throw error;
  }

  return (
    <main className="page-shell">
      <section className="page-section page-section--narrow">
        <WordDetailsCard word={word} />
        <TranslationOptionsList options={word.translation_options} />
      </section>
    </main>
  );
}
