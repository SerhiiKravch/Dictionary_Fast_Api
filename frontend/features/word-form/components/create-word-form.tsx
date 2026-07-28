"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { StatePanel } from "@/components/ui/state-panel";
import { Textarea } from "@/components/ui/textarea";
import { ApiClientError } from "@/services/api-client";
import { createWord } from "@/services/words";
import type { LanguageCode, PartOfSpeech, TranslationOptionCreate, WordOrigin } from "@/types/word";

type TranslationOptionDraft = {
  id: number;
  text: string;
  part_of_speech: PartOfSpeech;
  priority: number;
  usage_note: string;
};

const DEFAULT_OPTION: TranslationOptionDraft = {
  id: 1,
  text: "",
  part_of_speech: "other",
  priority: 1,
  usage_note: "",
};

type ValidationErrors = {
  sourceWord?: string;
  transcription?: string;
  primaryTranslation?: string;
  contextSentence?: string;
  direction?: string;
  translationOptions?: string;
};

export function CreateWordForm() {
  const router = useRouter();
  const [sourceWord, setSourceWord] = useState("");
  const [sourceLanguage, setSourceLanguage] = useState<LanguageCode>("en");
  const [targetLanguage, setTargetLanguage] = useState<LanguageCode>("uk");
  const [transcription, setTranscription] = useState("");
  const [primaryTranslation, setPrimaryTranslation] = useState("");
  const [contextSentence, setContextSentence] = useState("");
  const [origin, setOrigin] = useState<WordOrigin>("manual");
  const [translationOptions, setTranslationOptions] = useState<TranslationOptionDraft[]>([
    DEFAULT_OPTION,
  ]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});

  function updateOption(id: number, patch: Partial<TranslationOptionDraft>) {
    setTranslationOptions((current) =>
      current.map((option) => (option.id === id ? { ...option, ...patch } : option)),
    );
  }

  function addOption() {
    setTranslationOptions((current) => [
      ...current,
      {
        ...DEFAULT_OPTION,
        id: current[current.length - 1]?.id ? current[current.length - 1].id + 1 : 1,
      },
    ]);
  }

  function removeOption(id: number) {
    setTranslationOptions((current) => current.filter((option) => option.id !== id));
    setValidationErrors((current) => ({ ...current, translationOptions: undefined }));
  }

  function validateForm(): ValidationErrors {
    const errors: ValidationErrors = {};

    if (!sourceWord.trim()) {
      errors.sourceWord = "Source word is required.";
    }

    if (!transcription.trim()) {
      errors.transcription = "Transcription is required.";
    }

    if (!primaryTranslation.trim()) {
      errors.primaryTranslation = "Primary translation is required.";
    }

    if (!contextSentence.trim()) {
      errors.contextSentence = "Context sentence is required.";
    }

    if (sourceLanguage === targetLanguage) {
      errors.direction = "Source and target languages must be different.";
    }

    const partiallyFilledOption = translationOptions.some(
      (option) =>
        !option.text.trim() && (option.usage_note.trim() || option.priority !== 1 || option.part_of_speech !== "other"),
    );

    if (partiallyFilledOption) {
      errors.translationOptions =
        "Every translation option with extra data must also include translation text.";
    }

    return errors;
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    const nextValidationErrors = validateForm();
    setValidationErrors(nextValidationErrors);

    if (Object.keys(nextValidationErrors).length > 0) {
      return;
    }

    setIsSubmitting(true);

    const normalizedOptions: TranslationOptionCreate[] = translationOptions
      .map((option) => ({
        text: option.text.trim(),
        part_of_speech: option.part_of_speech,
        priority: option.priority,
        usage_note: option.usage_note.trim(),
      }))
      .filter((option) => option.text);

    try {
      const word = await createWord({
        source_word: sourceWord.trim(),
        source_language: sourceLanguage,
        target_language: targetLanguage,
        transcription: transcription.trim(),
        primary_translation: primaryTranslation.trim(),
        context_sentence: contextSentence.trim(),
        origin,
        translation_options: normalizedOptions,
      });

      router.push(`/words/${word.slug}`);
    } catch (error) {
      if (error instanceof ApiClientError) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Could not create the word.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Card className="stack-md">
        {Object.keys(validationErrors).length > 0 ? (
          <div className="message message--error stack-sm" role="alert" aria-live="assertive">
            <strong>Fix the highlighted fields before submitting.</strong>
            <p className="message">The form stays filled in, so you only need to correct the invalid parts.</p>
          </div>
        ) : null}

        <div className="form-grid">
          <Field
            label="Source word"
            htmlFor="source-word"
            error={validationErrors.sourceWord}
            hint="Use the exact source-language spelling you want to keep in the dictionary."
          >
            <Input
              value={sourceWord}
              onChange={(event) => {
                setSourceWord(event.target.value);
                setValidationErrors((current) => ({ ...current, sourceWord: undefined }));
              }}
              invalid={Boolean(validationErrors.sourceWord)}
              required
            />
          </Field>

          <Field
            label="Transcription"
            htmlFor="transcription"
            error={validationErrors.transcription}
            hint="Keep the pronunciation compact and readable for quick scanning later."
          >
            <Input
              value={transcription}
              onChange={(event) => {
                setTranscription(event.target.value);
                setValidationErrors((current) => ({ ...current, transcription: undefined }));
              }}
              invalid={Boolean(validationErrors.transcription)}
              required
            />
          </Field>

          <Field label="Source language" htmlFor="source-language">
            <Select
              value={sourceLanguage}
              onChange={(event) => {
                setSourceLanguage(event.target.value as LanguageCode);
                setValidationErrors((current) => ({ ...current, direction: undefined }));
              }}
            >
              <option value="en">English</option>
              <option value="uk">Ukrainian</option>
            </Select>
          </Field>

          <Field
            label="Target language"
            htmlFor="target-language"
            error={validationErrors.direction}
          >
            <Select
              value={targetLanguage}
              onChange={(event) => {
                setTargetLanguage(event.target.value as LanguageCode);
                setValidationErrors((current) => ({ ...current, direction: undefined }));
              }}
              invalid={Boolean(validationErrors.direction)}
            >
              <option value="uk">Ukrainian</option>
              <option value="en">English</option>
            </Select>
          </Field>

          <Field
            label="Primary translation"
            htmlFor="primary-translation"
            error={validationErrors.primaryTranslation}
            hint="This becomes the main meaning shown in the catalog and detail page."
          >
            <Input
              value={primaryTranslation}
              onChange={(event) => {
                setPrimaryTranslation(event.target.value);
                setValidationErrors((current) => ({ ...current, primaryTranslation: undefined }));
              }}
              invalid={Boolean(validationErrors.primaryTranslation)}
              required
            />
          </Field>

          <Field
            label="Origin"
            htmlFor="origin"
            hint="Keep this as manual for entries created directly from the frontend."
          >
            <Select
              value={origin}
              onChange={(event) => setOrigin(event.target.value as WordOrigin)}
            >
              <option value="manual">Manual</option>
              <option value="openai">OpenAI</option>
              <option value="imported">Imported</option>
            </Select>
          </Field>
        </div>

        <Field
          label="Context sentence"
          htmlFor="context-sentence"
          error={validationErrors.contextSentence}
          hint="Add one realistic example so the word is useful when you revisit it later."
        >
          <Textarea
            value={contextSentence}
            onChange={(event) => {
              setContextSentence(event.target.value);
              setValidationErrors((current) => ({ ...current, contextSentence: undefined }));
            }}
            invalid={Boolean(validationErrors.contextSentence)}
            rows={4}
            required
          />
        </Field>

        <div className="stack-sm">
          <div className="split-heading">
            <div>
              <span className="field-label">Translation options</span>
              <p className="supporting-text">
                Add alternative meanings and usage notes, or keep this section empty to save only
                the main translation.
              </p>
            </div>
            <Button type="button" onClick={addOption}>
              Add option
            </Button>
          </div>

          <div className="stack-sm">
            {translationOptions.length === 0 ? (
              <StatePanel
                eyebrow="No alternatives yet"
                title="Only the primary translation will be saved."
                description="Add an option if you want to keep synonyms, parts of speech, or usage notes alongside the main translation."
                actions={
                  <Button type="button" onClick={addOption} variant="primary">
                    Add first option
                  </Button>
                }
              />
            ) : (
              translationOptions.map((option) => (
                <div key={option.id} className="option-editor">
                  <div className="form-grid">
                    <Field label="Text" htmlFor={`option-text-${option.id}`}>
                      <Input
                        value={option.text}
                        onChange={(event) => updateOption(option.id, { text: event.target.value })}
                      />
                    </Field>

                    <Field label="Part of speech" htmlFor={`option-pos-${option.id}`}>
                      <Select
                        value={option.part_of_speech}
                        onChange={(event) =>
                          updateOption(option.id, {
                            part_of_speech: event.target.value as PartOfSpeech,
                          })
                        }
                      >
                        <option value="noun">noun</option>
                        <option value="verb">verb</option>
                        <option value="adjective">adjective</option>
                        <option value="adverb">adverb</option>
                        <option value="pronoun">pronoun</option>
                        <option value="preposition">preposition</option>
                        <option value="conjunction">conjunction</option>
                        <option value="interjection">interjection</option>
                        <option value="phrase">phrase</option>
                        <option value="other">other</option>
                      </Select>
                    </Field>

                    <Field label="Priority" htmlFor={`option-priority-${option.id}`}>
                      <Input
                        type="number"
                        min={1}
                        value={option.priority}
                        onChange={(event) =>
                          updateOption(option.id, { priority: Number(event.target.value) || 1 })
                        }
                      />
                    </Field>
                  </div>

                  <Field label="Usage note" htmlFor={`option-note-${option.id}`}>
                    <Textarea
                      rows={2}
                      value={option.usage_note}
                      onChange={(event) =>
                        updateOption(option.id, { usage_note: event.target.value })
                      }
                    />
                  </Field>

                  <Button type="button" onClick={() => removeOption(option.id)}>
                    Remove option
                  </Button>
                </div>
              ))
            )}
          </div>
          {validationErrors.translationOptions ? (
            <p className="field-error" aria-live="polite">
              {validationErrors.translationOptions}
            </p>
          ) : null}
        </div>

        {errorMessage ? (
          <div className="message message--error stack-sm" role="alert" aria-live="assertive">
            <strong>Word creation failed.</strong>
            <p className="message">{errorMessage}</p>
          </div>
        ) : null}

        <Button variant="primary" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Creating..." : "Create word"}
        </Button>
      </Card>
    </form>
  );
}
