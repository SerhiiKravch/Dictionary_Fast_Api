"use client";

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import GlobalError from "./error";
import WordDetailsError from "./words/[slug]/error";
import WordNotFound from "./words/[slug]/not-found";

describe("route-level states", () => {
  it("renders the global app error boundary and retries", async () => {
    const user = userEvent.setup();
    const reset = vi.fn();

    render(<GlobalError error={new Error("Boom")} reset={reset} />);

    expect(screen.getByText("Application error")).toBeVisible();
    expect(screen.getByText("Boom")).toBeVisible();

    await user.click(screen.getByRole("button", { name: "Try again" }));

    expect(reset).toHaveBeenCalled();
  });

  it("renders the word details route error boundary and retries", async () => {
    const user = userEvent.setup();
    const reset = vi.fn();

    render(<WordDetailsError error={new Error("Detail failed")} reset={reset} />);

    expect(screen.getByText("Detail error")).toBeVisible();
    expect(screen.getByText("Detail failed")).toBeVisible();

    await user.click(screen.getByRole("button", { name: "Retry entry" }));

    expect(reset).toHaveBeenCalled();
  });

  it("renders the word not found state", () => {
    render(<WordNotFound />);

    expect(screen.getByText("Word not found")).toBeVisible();
    expect(screen.getByText("This dictionary entry does not exist.")).toBeVisible();
    expect(screen.getByRole("link", { name: "Search again" })).toHaveAttribute("href", "/");
  });
});
