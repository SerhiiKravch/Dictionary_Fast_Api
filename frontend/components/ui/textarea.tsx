import type { TextareaHTMLAttributes } from "react";

import { cx } from "./utils";

type TextareaProps = TextareaHTMLAttributes<HTMLTextAreaElement> & {
  invalid?: boolean;
};

export function Textarea({ className, invalid = false, ...props }: TextareaProps) {
  return (
    <textarea className={cx("textarea-input", invalid && "is-invalid", className)} {...props} />
  );
}
