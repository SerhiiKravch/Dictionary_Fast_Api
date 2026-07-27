import type { ButtonHTMLAttributes, ReactNode } from "react";

import { cx } from "./utils";

type ButtonVariant = "primary" | "secondary";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: ButtonVariant;
};

export function buttonClassName(variant: ButtonVariant = "secondary", className?: string) {
  return cx("button", variant === "primary" && "button--primary", className);
}

export function Button({
  children,
  className,
  type = "button",
  variant = "secondary",
  ...props
}: ButtonProps) {
  return (
    <button className={buttonClassName(variant, className)} type={type} {...props}>
      {children}
    </button>
  );
}
