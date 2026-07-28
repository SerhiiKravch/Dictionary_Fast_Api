import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { TranslationOptionsList } from "@/features/word-details/components/translation-options-list";
import { WordDetailsCard } from "@/features/word-details/components/word-details-card";
import { ApiClientError } from "@/services/api-client";
import { getWordBySlug } from "@/services/words";
import type { WordRead } from "@/types/word";

type WordDetailsPageProps = {
  params: Promise<{
    slug: string;
  }>;
};

async function loadWordOrNull(slug: string): Promise<WordRead | null> {
  try {
    return await getWordBySlug(slug);
  } catch (error) {
    if (error instanceof ApiClientError && error.errorCode === "word_not_found") {
      return null;
    }

    throw error;
  }
}

export async function generateMetadata({ params }: WordDetailsPageProps): Promise<Metadata> {
  const { slug } = await params;
  const word = await loadWordOrNull(slug);

  if (!word) {
    return {
      title: "Word not found | Dictionary",
      description: "The requested dictionary entry could not be found.",
    };
  }

  return {
    title: `${word.source_word} — ${word.primary_translation} | Dictionary`,
    description: `Translation, transcription and usage example for ${word.source_word}.`,
  };
}

export default async function WordDetailsPage({ params }: WordDetailsPageProps) {
  const { slug } = await params;
  const word = await loadWordOrNull(slug);

  if (!word) {
    notFound();
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
