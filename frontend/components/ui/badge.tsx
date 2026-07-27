import type { ReactNode } from "react";

import { cx } from "./utils";

type BadgeTone = "default" | "muted";

type BadgeProps = {
  children: ReactNode;
  tone?: BadgeTone;
  className?: string;
};

export function Badge({ children, tone = "default", className }: BadgeProps) {
  return <span className={cx("badge", tone === "muted" && "badge--muted", className)}>{children}</span>;
}
