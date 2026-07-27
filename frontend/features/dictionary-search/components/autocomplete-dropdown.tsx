"use client";

type AutocompleteDropdownProps = {
  suggestions: string[];
  isLoading: boolean;
  activeIndex: number;
  query: string;
  onSelect: (value: string) => void;
};

export function AutocompleteDropdown({
  suggestions,
  isLoading,
  activeIndex,
  query,
  onSelect,
}: AutocompleteDropdownProps) {
  if (isLoading) {
    return <p className="message" aria-live="polite">Loading suggestions...</p>;
  }

  if (!query.trim()) {
    return null;
  }

  if (suggestions.length === 0) {
    return (
      <div className="empty-state empty-state--compact">
        <p>No suggestions found for &quot;{query.trim()}&quot;.</p>
      </div>
    );
  }

  return (
    <ul
      className="suggestions-list"
      aria-label="Autocomplete suggestions"
      role="listbox"
      id="dictionary-search-suggestions"
    >
      {suggestions.map((suggestion, index) => (
        <li key={suggestion}>
          <button
            className={index === activeIndex ? "suggestion-item is-active" : "suggestion-item"}
            type="button"
            role="option"
            aria-selected={index === activeIndex}
            onClick={() => onSelect(suggestion)}
            onMouseDown={(event) => event.preventDefault()}
          >
            {suggestion}
          </button>
        </li>
      ))}
    </ul>
  );
}
