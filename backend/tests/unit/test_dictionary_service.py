import pytest

from app.exceptions.dictionary import (
    EmptyWordError,
    InvalidDirectionError,
    SameLanguageDirectionError,
    WordAlreadyExistsError,
)
from app.models.enums import DifficultyLevel, InflectionType, LanguageCode, PartOfSpeech
from app.services import dictionary
from app.services.dictionary import (
    create_word_manually,
    get_word_by_slug,
    normalize_word,
    parse_direction,
    validate_language_direction,
)
from app.services.word_metadata_service import normalize_tags, validate_tag_name
from tests.factories import (
    make_translation_option_create,
    make_word_create,
    make_word_inflection_create,
)

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


def test_validate_tag_name_normalizes_value() -> None:
    assert validate_tag_name(" Spoken_Word ") == "spoken_word"


def test_validate_tag_name_rejects_invalid_characters() -> None:
    with pytest.raises(ValueError, match="letters, digits, hyphens, and underscores"):
        validate_tag_name("spoken word")


def test_normalize_tags_sorts_and_deduplicates() -> None:
    assert normalize_tags([" spoken", "common", "spoken"]) == ["common", "spoken"]


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
    assert len(word.senses) == 1
    assert word.senses[0].primary_translation == "яблуко"
    assert word.senses[0].part_of_speech == "noun"
    assert len(word.senses[0].example_sentences) == 1
    assert word.senses[0].example_sentences[0].source_text == "I ate an apple."


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


def test_create_word_manually_persists_difficulty_tags_and_inflections(db_session) -> None:
    payload = make_word_create(
        source_word="Run",
        primary_translation="бігти",
        context_sentence="I run every morning.",
        difficulty_level=DifficultyLevel.A2,
        tags=[" Spoken ", "common", "spoken"],
        inflections=[
            make_word_inflection_create(
                form_type=InflectionType.PAST_SIMPLE,
                value="ran",
            ),
            make_word_inflection_create(
                form_type=InflectionType.PAST_PARTICIPLE,
                value="run",
            ),
        ],
    )

    word = create_word_manually(db=db_session, payload=payload)

    assert word.difficulty_level == DifficultyLevel.A2.value
    assert [tag.name for tag in word.tags] == ["common", "spoken"]
    assert [(item.form_type, item.value) for item in word.inflections] == [
        (InflectionType.PAST_SIMPLE.value, "ran"),
        (InflectionType.PAST_PARTICIPLE.value, "run"),
    ]


def test_create_word_manually_creates_default_sense_without_translation_options(db_session) -> None:
    payload = make_word_create(
        source_word="banana",
        primary_translation="банан",
        context_sentence="I ate a banana.",
        translation_options=[],
    )

    word = create_word_manually(db=db_session, payload=payload)

    assert len(word.senses) == 1
    assert word.senses[0].part_of_speech == "other"
    assert word.senses[0].primary_translation == "банан"
    assert word.senses[0].example_sentences[0].source_text == "I ate a banana."


def test_get_word_by_slug_returns_word_with_senses_and_examples(db_session) -> None:
    created_word = create_word_manually(
        db=db_session,
        payload=make_word_create(
            source_word="speak",
            primary_translation="говорити",
            context_sentence="We speak every day.",
            translation_options=[
                make_translation_option_create(
                    text="говорити",
                    part_of_speech=PartOfSpeech.VERB,
                )
            ],
        ),
    )

    loaded_word = get_word_by_slug(db=db_session, slug=created_word.slug)

    assert len(loaded_word.senses) == 1
    assert loaded_word.senses[0].part_of_speech == "verb"
    assert loaded_word.senses[0].example_sentences[0].source_text == "We speak every day."


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
