from __future__ import annotations

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions.dictionary import WordAlreadyExistsError
from app.models.enums import LanguageCode, WordOrigin
from app.models.word import Word
from app.services.dictionary import create_word_manually
from tests.factories import make_word_create, make_word_create_payload

pytestmark = pytest.mark.integration


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
