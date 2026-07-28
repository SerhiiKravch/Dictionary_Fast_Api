"use client";

import type { LookupDirection } from "@/types/word";

type DirectionSwitcherProps = {
  value: LookupDirection;
  onChange: (value: LookupDirection) => void;
};

export function DirectionSwitcher({ value, onChange }: DirectionSwitcherProps) {
  return (
    <div className="stack-sm">
      <span className="field-label">Direction</span>
      <div className="segmented-control" role="radiogroup" aria-label="Translation direction">
        <button
          className={value === "en:uk" ? "segmented-control__item is-active" : "segmented-control__item"}
          type="button"
          onClick={() => onChange("en:uk")}
        >
          EN → UK
        </button>
        <button
          className={value === "uk:en" ? "segmented-control__item is-active" : "segmented-control__item"}
          type="button"
          onClick={() => onChange("uk:en")}
        >
          UK → EN
        </button>
      </div>
    </div>
  );
}
