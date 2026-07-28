import type { HTMLAttributes, ReactNode } from "react";

import { cx } from "./utils";

type CardProps = HTMLAttributes<HTMLElement> & {
  children: ReactNode;
  as?: "article" | "section" | "div";
  inset?: "default" | "compact";
};

export function Card({
  as: Component = "div",
  children,
  className,
  inset = "default",
  ...props
}: CardProps) {
  return (
    <Component
      className={cx("panel", inset === "compact" && "panel--compact", className)}
      {...props}
    >
      {children}
    </Component>
  );
}
