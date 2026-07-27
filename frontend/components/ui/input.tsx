import type { InputHTMLAttributes } from "react";

import { cx } from "./utils";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  invalid?: boolean;
};

export function Input({ className, invalid = false, ...props }: InputProps) {
  return <input className={cx("text-input", invalid && "is-invalid", className)} {...props} />;
}
