from __future__ import annotations

from app.models.enums import DifficultyLevel, InflectionType, LanguageCode, PartOfSpeech, WordOrigin
from app.schemas.word import TranslationOptionCreate, WordCreate, WordInflectionCreate


def make_translation_option_create(
    *,
    text: str = "яблуко",
    part_of_speech: PartOfSpeech = PartOfSpeech.NOUN,
    priority: int = 1,
    usage_note: str = "",
) -> TranslationOptionCreate:
    return TranslationOptionCreate(
        text=text,
        part_of_speech=part_of_speech,
        priority=priority,
        usage_note=usage_note,
    )


def make_word_create(
    *,
    source_word: str = "apple",
    source_language: LanguageCode = LanguageCode.ENGLISH,
    target_language: LanguageCode = LanguageCode.UKRAINIAN,
    transcription: str = "[ap-l]",
    primary_translation: str = "яблуко",
    context_sentence: str = "I ate an apple.",
    difficulty_level: DifficultyLevel | None = None,
    origin: WordOrigin = WordOrigin.MANUAL,
    tags: list[str] | None = None,
    inflections: list[WordInflectionCreate] | None = None,
    translation_options: list[TranslationOptionCreate] | None = None,
) -> WordCreate:
    return WordCreate(
        source_word=source_word,
        source_language=source_language,
        target_language=target_language,
        transcription=transcription,
        primary_translation=primary_translation,
        context_sentence=context_sentence,
        difficulty_level=difficulty_level,
        origin=origin,
        tags=tags or [],
        inflections=inflections or [],
        translation_options=translation_options or [],
    )


def make_word_inflection_create(
    *,
    form_type: InflectionType = InflectionType.PLURAL,
    value: str = "apples",
    notes: str = "",
) -> WordInflectionCreate:
    return WordInflectionCreate(
        form_type=form_type,
        value=value,
        notes=notes,
    )


def make_word_create_payload(**overrides: object) -> dict[str, object]:
    payload = {
        "source_word": "apple",
        "source_language": "en",
        "target_language": "uk",
        "transcription": "[ap-l]",
        "primary_translation": "яблуко",
        "context_sentence": "I ate an apple.",
        "difficulty_level": None,
        "origin": "manual",
        "tags": [],
        "inflections": [],
        "translation_options": [],
    }
    payload.update(overrides)
    return payload
