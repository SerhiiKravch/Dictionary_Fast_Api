from __future__ import annotations

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from alembic import command
from alembic.config import Config
from app.exceptions.dictionary import WordAlreadyExistsError
from app.models.enums import LanguageCode, WordOrigin
from app.models.word import Word
from app.services import dictionary
from app.services.dictionary import create_word_manually
from tests.factories import make_word_create, make_word_create_payload
from tests.fakes import FakeOpenAIService
from tests.integration.conftest import POSTGRES_TEST_DATABASE_URL

pytestmark = pytest.mark.integration


def make_alembic_config() -> Config:
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", POSTGRES_TEST_DATABASE_URL)
    return alembic_config


def test_postgres_create_word_rejects_duplicate_direction(postgres_db_session) -> None:
    payload = make_word_create(
        source_word="apple",
        source_language=LanguageCode.ENGLISH,
        target_language=LanguageCode.UKRAINIAN,
    )

    create_word_manually(db=postgres_db_session, payload=payload)

    with pytest.raises(WordAlreadyExistsError) as exc_info:
        create_word_manually(db=postgres_db_session, payload=payload)

    assert "selected translation direction" in str(exc_info.value).lower()


def test_postgres_enforces_different_languages_check_constraint(postgres_db_session) -> None:
    invalid_word = Word(
        source_word="apple",
        source_language=LanguageCode.ENGLISH.value,
        target_language=LanguageCode.ENGLISH.value,
        slug="apple-en-en",
        transcription="[ap-l]",
        primary_translation="apple",
        context_sentence="Apple stays apple.",
        origin=WordOrigin.MANUAL.value,
    )

    postgres_db_session.add(invalid_word)

    with pytest.raises(IntegrityError):
        postgres_db_session.commit()

    postgres_db_session.rollback()


def test_postgres_api_words_endpoint_supports_filters_and_search(postgres_client) -> None:
    postgres_client.post("/api/words", json=make_word_create_payload(source_word="apple"))
    postgres_client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="pineapple",
            primary_translation="ананас",
            context_sentence="Pineapple is sweet.",
            origin="imported",
        ),
    )
    postgres_client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="кіт",
            source_language="uk",
            target_language="en",
            primary_translation="cat",
            context_sentence="Це кіт.",
        ),
    )

    response = postgres_client.get(
        "/api/words?source_language=en&target_language=uk&origin=imported&search=apple"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert [item["source_word"] for item in body["items"]] == ["pineapple"]


def test_postgres_api_word_detail_returns_translation_options(postgres_client) -> None:
    create_response = postgres_client.post(
        "/api/words",
        json=make_word_create_payload(
            translation_options=[
                {
                    "text": "яблуко",
                    "part_of_speech": "noun",
                    "priority": 1,
                    "usage_note": "basic",
                }
            ],
        ),
    )
    slug = create_response.json()["slug"]

    response = postgres_client.get(f"/api/words/{slug}")

    assert response.status_code == 200
    body = response.json()
    assert body["slug"] == slug
    assert body["translation_options"][0]["text"] == "яблуко"


def test_postgres_lookup_returns_structured_senses(postgres_client, monkeypatch) -> None:
    monkeypatch.setattr(dictionary, "OpenAIService", FakeOpenAIService)

    response = postgres_client.post("/lookup", json={"word": "test", "direction": "en:uk"})

    assert response.status_code == 200
    body = response.json()
    assert body["primary_translation"] == "тест"
    assert len(body["senses"]) == 1
    assert body["senses"][0]["primary_translation"] == "тест"
    assert body["senses"][0]["example_sentences"][0]["source_text"] == "test sentence"


def test_postgres_backfill_migration_creates_word_sense_and_example(postgres_engine) -> None:
    alembic_config = make_alembic_config()
    command.downgrade(alembic_config, "6f8e9a0b1c2d")

    try:
        with postgres_engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO words (
                        id,
                        source_word,
                        source_language,
                        target_language,
                        slug,
                        transcription,
                        primary_translation,
                        context_sentence,
                        difficulty_level,
                        origin,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        1,
                        'apple',
                        'en',
                        'uk',
                        'apple-en-uk',
                        '[ap-l]',
                        'яблуко',
                        'I ate an apple.',
                        NULL,
                        'manual',
                        now(),
                        now()
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    INSERT INTO translation_options (
                        word_id,
                        text,
                        part_of_speech,
                        priority,
                        usage_note
                    )
                    VALUES (
                        1,
                        'яблуко',
                        'noun',
                        1,
                        'basic'
                    )
                    """
                )
            )

        command.upgrade(alembic_config, "head")

        with postgres_engine.connect() as connection:
            sense_row = (
                connection.execute(
                    text(
                        """
                    SELECT part_of_speech, primary_translation, position
                    FROM word_senses
                    WHERE word_id = 1
                    """
                    )
                )
                .mappings()
                .one()
            )
            example_row = (
                connection.execute(
                    text(
                        """
                    SELECT source_text, translated_text, position
                    FROM example_sentences
                    WHERE sense_id = (
                        SELECT id FROM word_senses WHERE word_id = 1
                    )
                    """
                    )
                )
                .mappings()
                .one()
            )

        assert sense_row["part_of_speech"] == "noun"
        assert sense_row["primary_translation"] == "яблуко"
        assert sense_row["position"] == 1
        assert example_row["source_text"] == "I ate an apple."
        assert example_row["translated_text"] == ""
        assert example_row["position"] == 1
    finally:
        command.upgrade(alembic_config, "head")
