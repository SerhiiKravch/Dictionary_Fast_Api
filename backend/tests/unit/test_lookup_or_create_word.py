import pytest

from app.models.enums import LanguageCode
from app.schemas.word import WordLookupRequest
from app.services import dictionary
from app.services.dictionary import create_word_manually, lookup_or_create_word
from tests.factories import make_word_create
from tests.fakes import FailingOpenAIService, FakeOpenAIService

pytestmark = pytest.mark.unit


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
    existing_payload = make_word_create(
        source_word="apple",
        source_language=LanguageCode.ENGLISH,
        target_language=LanguageCode.UKRAINIAN,
        transcription="[ˈæp.əl]",
        primary_translation="яблуко",
        context_sentence="I ate an apple.",
        origin="manual",
    )

    created_word = create_word_manually(db=db_session, payload=existing_payload)

    monkeypatch.setattr(dictionary, "OpenAIService", FailingOpenAIService)

    lookup_payload = WordLookupRequest(word="apple", direction="en:uk")
    result = lookup_or_create_word(db=db_session, payload=lookup_payload)

    assert result.id == created_word.id
    assert result.source_word == "apple"
    assert result.primary_translation == "яблуко"
