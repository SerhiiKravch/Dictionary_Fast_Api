"use client";

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiClientError } from "@/services/api-client";

import { CreateWordForm } from "./create-word-form";

const pushMock = vi.hoisted(() => vi.fn());
const createWordMock = vi.hoisted(() => vi.fn());

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

vi.mock("@/services/words", () => ({
  createWord: createWordMock,
}));

describe("CreateWordForm", () => {
  beforeEach(() => {
    createWordMock.mockReset();
    pushMock.mockReset();
  });

  it("shows validation errors and does not submit invalid data", async () => {
    render(<CreateWordForm />);

    fireEvent.submit(screen.getByRole("button", { name: "Create word" }).closest("form")!);

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Fix the highlighted fields before submitting.",
    );
    expect(screen.getByText("Source word is required.")).toBeVisible();
    expect(screen.getByText("Transcription is required.")).toBeVisible();
    expect(screen.getByText("Primary translation is required.")).toBeVisible();
    expect(screen.getByText("Context sentence is required.")).toBeVisible();
    expect(createWordMock).not.toHaveBeenCalled();
  });

  it("submits normalized data and redirects to the new word page", async () => {
    const user = userEvent.setup();

    createWordMock.mockResolvedValue({ slug: "hello" });

    render(<CreateWordForm />);

    await user.type(screen.getByLabelText("Source word"), "  hello  ");
    fireEvent.change(screen.getByLabelText("Transcription"), { target: { value: "  [həˈləʊ] " } });
    await user.type(screen.getByLabelText("Primary translation"), " привіт ");
    await user.type(screen.getByLabelText("Context sentence"), "  Hello there. ");

    await user.type(screen.getByLabelText("Text"), " greeting ");
    await user.type(screen.getByLabelText("Usage note"), " informal ");

    await user.click(screen.getByRole("button", { name: "Create word" }));

    await waitFor(() => {
      expect(createWordMock).toHaveBeenCalledWith({
        source_word: "hello",
        source_language: "en",
        target_language: "uk",
        transcription: "[həˈləʊ]",
        primary_translation: "привіт",
        context_sentence: "Hello there.",
        origin: "manual",
        translation_options: [
          {
            text: "greeting",
            part_of_speech: "other",
            priority: 1,
            usage_note: "informal",
          },
        ],
      });
    });

    expect(pushMock).toHaveBeenCalledWith("/words/hello");
  });

  it("renders backend errors without losing form state", async () => {
    const user = userEvent.setup();

    createWordMock.mockRejectedValue(
      new ApiClientError({
        message: "This word already exists for the selected direction.",
        status: 409,
        errorCode: "word_already_exists",
        details: null,
      }),
    );

    render(<CreateWordForm />);

    await user.type(screen.getByLabelText("Source word"), "hello");
    fireEvent.change(screen.getByLabelText("Transcription"), { target: { value: "[həˈləʊ]" } });
    await user.type(screen.getByLabelText("Primary translation"), "привіт");
    await user.type(screen.getByLabelText("Context sentence"), "Hello there.");

    await user.click(screen.getByRole("button", { name: "Create word" }));

    expect(await screen.findByText("Word creation failed.")).toBeVisible();
    expect(
      screen.getByText("This word already exists for the selected direction."),
    ).toBeVisible();
    expect(screen.getByLabelText("Source word")).toHaveValue("hello");
    expect(pushMock).not.toHaveBeenCalled();
  });
});
