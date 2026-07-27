"use client";

import { useState } from "react";
import { usePathname, useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
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
    <form onSubmit={handleSubmit}>
      <Card className="filters-grid">
        <Field label="Search" htmlFor="search">
          <Input
            id="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="apple"
          />
        </Field>

        <Field label="Source" htmlFor="source-language">
          <Select
            id="source-language"
            value={sourceLanguage}
            onChange={(event) => setSourceLanguage(event.target.value)}
          >
            <option value="">Any</option>
            <option value="en">English</option>
            <option value="uk">Ukrainian</option>
          </Select>
        </Field>

        <Field label="Target" htmlFor="target-language">
          <Select
            id="target-language"
            value={targetLanguage}
            onChange={(event) => setTargetLanguage(event.target.value)}
          >
            <option value="">Any</option>
            <option value="en">English</option>
            <option value="uk">Ukrainian</option>
          </Select>
        </Field>

        <Field label="Origin" htmlFor="origin">
          <Select id="origin" value={origin} onChange={(event) => setOrigin(event.target.value)}>
            <option value="">Any</option>
            <option value="manual">Manual</option>
            <option value="openai">OpenAI</option>
            <option value="imported">Imported</option>
          </Select>
        </Field>

        <div className="filters-actions">
          <Button variant="primary" type="submit">
            Apply filters
          </Button>
        </div>
      </Card>
    </form>
  );
}
