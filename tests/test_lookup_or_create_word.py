from app.models.enums import LanguageCode, PartOfSpeech
from app.schemas.word import (
    GeneratedTranslationOption,
    GeneratedWordPayload,
    TranslationOptionCreate,
    WordCreate,
    WordLookupRequest,
)
from app.services import dictionary
from app.services.dictionary import create_word_manually, lookup_or_create_word


class FakeOpenAIService:
    def generate_word_payload(self, word, source_language, target_language):
        return GeneratedWordPayload(
            source_word=word,
            source_language=source_language,
            target_language=target_language,
            transcription="[test]",
            primary_translation="тест",
            context_sentence="test sentence",
            origin="openai",
            translation_options=[
                GeneratedTranslationOption(
                    text="тест",
                    part_of_speech=PartOfSpeech.NOUN,
                    priority=1,
                    usage_note="",
                )
            ],
        )


class FailingOpenAIService:
    def __init__(self) -> None:
        raise AssertionError("OpenAIService should not be called when word already exists")


def test_lookup_or_create_word_creates_when_missing(db_session, monkeypatch) -> None:
    monkeypatch.setattr(dictionary, "OpenAIService", FakeOpenAIService)

    payload = WordLookupRequest(word="test", direction="en:uk")
    word = dictionary.lookup_or_create_word(db_session, payload)

    assert word.source_word == "test"
    assert word.primary_translation == "тест"


def test_lookup_or_create_word_returns_existing_without_openai(
    db_session,
    monkeypatch,
) -> None:
    existing_payload = WordCreate(
        source_word="apple",
        source_language=LanguageCode.ENGLISH,
        target_language=LanguageCode.UKRAINIAN,
        transcription="[ˈæp.əl]",
        primary_translation="яблуко",
        context_sentence="I ate an apple.",
        origin="manual",
        translation_options=[
            TranslationOptionCreate(
                text="яблуко",
                priority=1,
                usage_note="",
            )
        ],
    )

    created_word = create_word_manually(db=db_session, payload=existing_payload)

    monkeypatch.setattr(dictionary, "OpenAIService", FailingOpenAIService)

    lookup_payload = WordLookupRequest(word="apple", direction="en:uk")
    result = lookup_or_create_word(db=db_session, payload=lookup_payload)

    assert result.id == created_word.id
    assert result.source_word == "apple"
    assert result.primary_translation == "яблуко"
