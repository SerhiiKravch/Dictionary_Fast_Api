"use client";

import { useState } from "react";
import { usePathname, useRouter } from "next/navigation";

import type { WordsQueryParams } from "@/types/word";

type WordsFiltersProps = {
  filters: WordsQueryParams;
};

export function WordsFilters({ filters }: WordsFiltersProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [search, setSearch] = useState(filters.search ?? "");
  const [sourceLanguage, setSourceLanguage] = useState(filters.source_language ?? "");
  const [targetLanguage, setTargetLanguage] = useState(filters.target_language ?? "");
  const [origin, setOrigin] = useState(filters.origin ?? "");

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const params = new URLSearchParams();

    if (search.trim()) {
      params.set("search", search.trim());
    }
    if (sourceLanguage) {
      params.set("source_language", sourceLanguage);
    }
    if (targetLanguage) {
      params.set("target_language", targetLanguage);
    }
    if (origin) {
      params.set("origin", origin);
    }
    params.set("limit", String(filters.limit ?? 20));
    params.set("offset", "0");

    router.push(params.toString() ? `${pathname}?${params.toString()}` : pathname);
  }

  return (
    <form className="panel filters-grid" onSubmit={handleSubmit}>
      <div className="stack-sm">
        <label className="field-label" htmlFor="search">
          Search
        </label>
        <input
          id="search"
          className="text-input"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="apple"
        />
      </div>

      <div className="stack-sm">
        <label className="field-label" htmlFor="source-language">
          Source
        </label>
        <select
          id="source-language"
          className="select-input"
          value={sourceLanguage}
          onChange={(event) => setSourceLanguage(event.target.value)}
        >
          <option value="">Any</option>
          <option value="en">English</option>
          <option value="uk">Ukrainian</option>
        </select>
      </div>

      <div className="stack-sm">
        <label className="field-label" htmlFor="target-language">
          Target
        </label>
        <select
          id="target-language"
          className="select-input"
          value={targetLanguage}
          onChange={(event) => setTargetLanguage(event.target.value)}
        >
          <option value="">Any</option>
          <option value="en">English</option>
          <option value="uk">Ukrainian</option>
        </select>
      </div>

      <div className="stack-sm">
        <label className="field-label" htmlFor="origin">
          Origin
        </label>
        <select
          id="origin"
          className="select-input"
          value={origin}
          onChange={(event) => setOrigin(event.target.value)}
        >
          <option value="">Any</option>
          <option value="manual">Manual</option>
          <option value="openai">OpenAI</option>
          <option value="imported">Imported</option>
        </select>
      </div>

      <div className="filters-actions">
        <button className="button button--primary" type="submit">
          Apply filters
        </button>
      </div>
    </form>
  );
}
