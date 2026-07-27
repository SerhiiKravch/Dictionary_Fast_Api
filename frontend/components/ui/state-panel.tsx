import type { HTMLAttributes, ReactNode } from "react";

import { Card } from "./card";
import { cx } from "./utils";

type StatePanelTone = "default" | "error";

type StatePanelProps = HTMLAttributes<HTMLElement> & {
  eyebrow?: string;
  title: string;
  description: string;
  actions?: ReactNode;
  tone?: StatePanelTone;
};

export function StatePanel({
  eyebrow,
  title,
  description,
  actions,
  className,
  tone = "default",
  ...props
}: StatePanelProps) {
  return (
    <Card
      className={cx("state-panel", tone === "error" && "state-panel--error", className)}
      {...props}
    >
      <div className="stack-sm">
        {eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}
        <h2>{title}</h2>
        <p className="message">{description}</p>
      </div>

      {actions ? <div className="actions-row">{actions}</div> : null}
    </Card>
  );
}
