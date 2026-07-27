"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { ApiClientError } from "@/services/api-client";
import { getAutocomplete, lookupWord } from "@/services/words";
import type { LookupDirection } from "@/types/word";

import { AutocompleteDropdown } from "./autocomplete-dropdown";
import { DirectionSwitcher } from "./direction-switcher";

const AUTOCOMPLETE_DELAY_MS = 250;

export function DictionarySearchForm() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [direction, setDirection] = useState<LookupDirection>("en:uk");
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [isLoading, setIsLoading] = useState(false);
  const [isAutocompleteLoading, setIsAutocompleteLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const normalizedQuery = query.trim();

    if (!normalizedQuery) {
      return;
    }

    const timeoutId = window.setTimeout(async () => {
      setIsAutocompleteLoading(true);

      try {
        const response = await getAutocomplete(normalizedQuery);
        setSuggestions(response.results);
        setActiveIndex(response.results.length > 0 ? 0 : -1);
      } catch {
        setSuggestions([]);
        setActiveIndex(-1);
      } finally {
        setIsAutocompleteLoading(false);
      }
    }, AUTOCOMPLETE_DELAY_MS);

    return () => window.clearTimeout(timeoutId);
  }, [query]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!query.trim()) {
      setErrorMessage("Enter a word before searching.");
      return;
    }

    if (suggestions.length > 0 && activeIndex >= 0) {
      handleSuggestionSelect(suggestions[activeIndex]);
      return;
    }

    setErrorMessage("");
    setIsLoading(true);

    try {
      const word = await lookupWord({
        word: query.trim(),
        direction,
      });

      router.push(`/words/${word.slug}`);
    } catch (error) {
      if (error instanceof ApiClientError) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Lookup failed. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  function handleSuggestionSelect(value: string) {
    setQuery(value);
    setSuggestions([]);
    setActiveIndex(-1);
    setErrorMessage("");
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (suggestions.length === 0) {
      if (event.key === "Escape") {
        setSuggestions([]);
        setActiveIndex(-1);
      }
      return;
    }

    if (event.key === "ArrowDown") {
      event.preventDefault();
      setActiveIndex((current) => (current + 1) % suggestions.length);
      return;
    }

    if (event.key === "ArrowUp") {
      event.preventDefault();
      setActiveIndex((current) => (current <= 0 ? suggestions.length - 1 : current - 1));
      return;
    }

    if (event.key === "Enter" && activeIndex >= 0) {
      event.preventDefault();
      handleSuggestionSelect(suggestions[activeIndex]);
      return;
    }

    if (event.key === "Escape") {
      setSuggestions([]);
      setActiveIndex(-1);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Card className="stack-md">
        <Field
          label="Search word"
          htmlFor="dictionary-search"
          error={errorMessage || undefined}
          hint="Type an English or Ukrainian word and use arrows to navigate suggestions."
        >
          <Input
            type="text"
            value={query}
            onChange={(event) => {
              const nextValue = event.target.value;
              setQuery(nextValue);

              if (!nextValue.trim()) {
                setSuggestions([]);
                setActiveIndex(-1);
              }
            }}
            onKeyDown={handleKeyDown}
            placeholder="Type apple or кіт"
            autoComplete="off"
            aria-autocomplete="list"
            aria-controls="dictionary-search-suggestions"
            invalid={Boolean(errorMessage)}
          />
        </Field>
        <AutocompleteDropdown
          suggestions={suggestions}
          isLoading={isAutocompleteLoading}
          activeIndex={activeIndex}
          query={query}
          onSelect={handleSuggestionSelect}
        />

        <DirectionSwitcher value={direction} onChange={setDirection} />

        <Button variant="primary" type="submit" disabled={isLoading}>
          {isLoading ? "Looking up..." : "Find translation"}
        </Button>
      </Card>
    </form>
  );
}
