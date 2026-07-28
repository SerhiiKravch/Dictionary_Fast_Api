import { cloneElement, isValidElement } from "react";
import type { ReactElement, ReactNode } from "react";

import { cx } from "./utils";

type FieldProps = {
  label: string;
  htmlFor?: string;
  error?: string;
  hint?: string;
  className?: string;
  children: ReactNode;
};

export function Field({ label, htmlFor, error, hint, className, children }: FieldProps) {
  const describedBy = error
    ? htmlFor
      ? `${htmlFor}-error`
      : undefined
    : hint
      ? htmlFor
        ? `${htmlFor}-hint`
        : undefined
      : undefined;

  const enhancedChild =
    isValidElement(children)
      ? cloneElement(children as ReactElement<Record<string, unknown>>, {
          id: htmlFor ?? (children.props as { id?: string }).id,
          "aria-invalid":
            error ? true : (children.props as { "aria-invalid"?: boolean })["aria-invalid"],
          "aria-describedby":
            describedBy ??
            (children.props as { "aria-describedby"?: string })["aria-describedby"],
        })
      : children;

  return (
    <div className={cx("field-root", "stack-sm", className)}>
      <label className="field-label" htmlFor={htmlFor}>
        {label}
      </label>
      {enhancedChild as ReactNode}
      {hint ? (
        <p className="field-hint" id={htmlFor ? `${htmlFor}-hint` : undefined}>
          {hint}
        </p>
      ) : null}
      {error ? (
        <p className="field-error" id={htmlFor ? `${htmlFor}-error` : undefined}>
          {error}
        </p>
      ) : null}
    </div>
  );
}
