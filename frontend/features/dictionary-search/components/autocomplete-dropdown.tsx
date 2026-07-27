"use client";

type AutocompleteDropdownProps = {
  suggestions: string[];
  isLoading: boolean;
  onSelect: (value: string) => void;
};

export function AutocompleteDropdown({
  suggestions,
  isLoading,
  onSelect,
}: AutocompleteDropdownProps) {
  if (isLoading) {
    return <p className="message">Loading suggestions...</p>;
  }

  if (suggestions.length === 0) {
    return null;
  }

  return (
    <ul className="suggestions-list" aria-label="Autocomplete suggestions">
      {suggestions.map((suggestion) => (
        <li key={suggestion}>
          <button
            className="suggestion-item"
            type="button"
            onClick={() => onSelect(suggestion)}
          >
            {suggestion}
          </button>
        </li>
      ))}
    </ul>
  );
}
