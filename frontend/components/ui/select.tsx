import type { SelectHTMLAttributes } from "react";

import { cx } from "./utils";

type SelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  invalid?: boolean;
};

export function Select({ className, invalid = false, ...props }: SelectProps) {
  return <select className={cx("select-input", invalid && "is-invalid", className)} {...props} />;
}
