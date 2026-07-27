"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

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
    <form className="panel stack-md" onSubmit={handleSubmit}>
      {Object.keys(validationErrors).length > 0 ? (
        <div className="message message--error" role="alert">
          <strong>Fix the highlighted fields before submitting.</strong>
        </div>
      ) : null}

      <div className="form-grid">
        <Field label="Source word">
          <input
            className={validationErrors.sourceWord ? "text-input is-invalid" : "text-input"}
            value={sourceWord}
            onChange={(event) => {
              setSourceWord(event.target.value);
              setValidationErrors((current) => ({ ...current, sourceWord: undefined }));
            }}
            required
          />
          {validationErrors.sourceWord ? (
            <p className="field-error">{validationErrors.sourceWord}</p>
          ) : null}
        </Field>

        <Field label="Transcription">
          <input
            className={validationErrors.transcription ? "text-input is-invalid" : "text-input"}
            value={transcription}
            onChange={(event) => {
              setTranscription(event.target.value);
              setValidationErrors((current) => ({ ...current, transcription: undefined }));
            }}
            required
          />
          {validationErrors.transcription ? (
            <p className="field-error">{validationErrors.transcription}</p>
          ) : null}
        </Field>

        <Field label="Source language">
          <select
            className="select-input"
            value={sourceLanguage}
            onChange={(event) => {
              setSourceLanguage(event.target.value as LanguageCode);
              setValidationErrors((current) => ({ ...current, direction: undefined }));
            }}
          >
            <option value="en">English</option>
            <option value="uk">Ukrainian</option>
          </select>
        </Field>

        <Field label="Target language">
          <select
            className={validationErrors.direction ? "select-input is-invalid" : "select-input"}
            value={targetLanguage}
            onChange={(event) => {
              setTargetLanguage(event.target.value as LanguageCode);
              setValidationErrors((current) => ({ ...current, direction: undefined }));
            }}
          >
            <option value="uk">Ukrainian</option>
            <option value="en">English</option>
          </select>
          {validationErrors.direction ? (
            <p className="field-error">{validationErrors.direction}</p>
          ) : null}
        </Field>

        <Field label="Primary translation">
          <input
            className={validationErrors.primaryTranslation ? "text-input is-invalid" : "text-input"}
            value={primaryTranslation}
            onChange={(event) => {
              setPrimaryTranslation(event.target.value);
              setValidationErrors((current) => ({ ...current, primaryTranslation: undefined }));
            }}
            required
          />
          {validationErrors.primaryTranslation ? (
            <p className="field-error">{validationErrors.primaryTranslation}</p>
          ) : null}
        </Field>

        <Field label="Origin">
          <select
            className="select-input"
            value={origin}
            onChange={(event) => setOrigin(event.target.value as WordOrigin)}
          >
            <option value="manual">Manual</option>
            <option value="openai">OpenAI</option>
            <option value="imported">Imported</option>
          </select>
        </Field>
      </div>

      <Field label="Context sentence">
        <textarea
          className={validationErrors.contextSentence ? "textarea-input is-invalid" : "textarea-input"}
          value={contextSentence}
          onChange={(event) => {
            setContextSentence(event.target.value);
            setValidationErrors((current) => ({ ...current, contextSentence: undefined }));
          }}
          rows={4}
          required
        />
        {validationErrors.contextSentence ? (
          <p className="field-error">{validationErrors.contextSentence}</p>
        ) : null}
      </Field>

      <div className="stack-sm">
        <div className="split-heading">
          <div>
            <span className="field-label">Translation options</span>
            <p className="supporting-text">
              Add alternative meanings and usage notes, or leave the option empty to save only the
              main translation.
            </p>
          </div>
          <button className="button" type="button" onClick={addOption}>
            Add option
          </button>
        </div>

        <div className="stack-sm">
          {translationOptions.map((option) => (
            <div key={option.id} className="option-editor">
              <div className="form-grid">
                <Field label="Text">
                  <input
                    className="text-input"
                    value={option.text}
                    onChange={(event) => updateOption(option.id, { text: event.target.value })}
                  />
                </Field>

                <Field label="Part of speech">
                  <select
                    className="select-input"
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
                  </select>
                </Field>

                <Field label="Priority">
                  <input
                    className="text-input"
                    type="number"
                    min={1}
                    value={option.priority}
                    onChange={(event) =>
                      updateOption(option.id, { priority: Number(event.target.value) || 1 })
                    }
                  />
                </Field>
              </div>

              <Field label="Usage note">
                <textarea
                  className="textarea-input"
                  rows={2}
                  value={option.usage_note}
                  onChange={(event) => updateOption(option.id, { usage_note: event.target.value })}
                />
              </Field>

              {translationOptions.length > 1 ? (
                <button className="button" type="button" onClick={() => removeOption(option.id)}>
                  Remove option
                </button>
              ) : null}
            </div>
          ))}
        </div>
        {validationErrors.translationOptions ? (
          <p className="field-error">{validationErrors.translationOptions}</p>
        ) : null}
      </div>

      {errorMessage ? <p className="message message--error">{errorMessage}</p> : null}

      <button className="button button--primary" type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Creating..." : "Create word"}
      </button>
    </form>
  );
}

type FieldProps = Readonly<{
  label: string;
  children: React.ReactNode;
}>;

function Field({ label, children }: FieldProps) {
  return (
    <label className="stack-sm">
      <span className="field-label">{label}</span>
      {children}
    </label>
  );
}
