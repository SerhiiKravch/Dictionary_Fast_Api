import pytest

from app.exceptions.dictionary import (
    EmptyWordError,
    InvalidDirectionError,
    SameLanguageDirectionError,
    WordAlreadyExistsError,
)
from app.models.enums import LanguageCode
from app.services import dictionary
from app.services.dictionary import (
    create_word_manually,
    normalize_word,
    parse_direction,
    validate_language_direction,
)
from tests.factories import make_translation_option_create, make_word_create

pytestmark = pytest.mark.unit


def test_normalize_word_strips_and_lowercase() -> None:
    assert normalize_word("  Apple  ") == "apple"


def test_normalize_word_raises_for_empty() -> None:
    with pytest.raises(EmptyWordError):
        normalize_word("   ")


def test_validate_language_direction_same_directions() -> None:
    with pytest.raises(SameLanguageDirectionError):
        validate_language_direction(LanguageCode.ENGLISH, LanguageCode.ENGLISH)


def test_validate_language_direction_differnt_directions() -> None:
    validate_language_direction(LanguageCode.ENGLISH, LanguageCode.UKRAINIAN)


def test_parse_direction_returns_language_codes() -> None:
    source, target = parse_direction("en:uk")
    assert source == LanguageCode.ENGLISH
    assert target == LanguageCode.UKRAINIAN


def test_parse_direction_invalid_format() -> None:
    with pytest.raises(InvalidDirectionError):
        parse_direction("en-uk")


def test_parse_direction_rejects_same_languages() -> None:
    with pytest.raises(SameLanguageDirectionError):
        parse_direction("en:en")


def test_create_word_manually_persists_word_and_options(db_session) -> None:
    payload = make_word_create(
        source_word="Apple",
        source_language=LanguageCode.ENGLISH,
        target_language=LanguageCode.UKRAINIAN,
        transcription="[ap-l]",
        primary_translation="яблуко",
        context_sentence="I ate an apple.",
        origin="manual",
        translation_options=[
            make_translation_option_create(
                text="яблуко",
                priority=1,
                usage_note="basic",
            )
        ],
    )

    word = create_word_manually(db=db_session, payload=payload)

    assert word.id is not None
    assert word.source_word == "apple"
    assert word.slug.startswith("apple-en-uk")
    assert len(word.translation_options) == 1


def test_create_word_manually_rejects_duplicate_direction(db_session) -> None:
    payload = make_word_create(
        source_word="Apple",
        source_language=LanguageCode.ENGLISH,
        target_language=LanguageCode.UKRAINIAN,
        transcription="[ap-l]",
        primary_translation="яблуко",
        context_sentence="I ate an apple.",
        origin="manual",
        translation_options=[
            make_translation_option_create(
                text="яблуко",
                priority=1,
                usage_note="basic",
            )
        ],
    )

    create_word_manually(db=db_session, payload=payload)

    with pytest.raises(WordAlreadyExistsError):
        create_word_manually(db=db_session, payload=payload)


def test_create_word_manually_adds_suffix_on_slug_conflict(db_session, monkeypatch) -> None:
    monkeypatch.setattr(dictionary, "build_base_slug", lambda *args, **kwargs: "fixed-slug")

    first = make_word_create(
        source_word="apple",
        source_language=LanguageCode.ENGLISH,
        target_language=LanguageCode.UKRAINIAN,
        transcription="a",
        primary_translation="яблуко",
        context_sentence="one",
        origin="manual",
        translation_options=[],
    )
    second = make_word_create(
        source_word="banana",
        source_language=LanguageCode.ENGLISH,
        target_language=LanguageCode.UKRAINIAN,
        transcription="b",
        primary_translation="банан",
        context_sentence="two",
        origin="manual",
        translation_options=[],
    )

    word1 = dictionary.create_word_manually(db_session, first)
    word2 = dictionary.create_word_manually(db_session, second)

    assert word1.slug == "fixed-slug"
    assert word2.slug.startswith("fixed-slug-")
    assert word1.slug != word2.slug
