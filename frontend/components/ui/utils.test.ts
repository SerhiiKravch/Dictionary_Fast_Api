import { describe, expect, it } from "vitest";

import { cx } from "./utils";

describe("cx", () => {
  it("joins only truthy class names", () => {
    expect(cx("panel", false, undefined, "stack-md", null, "")).toBe("panel stack-md");
  });
});
