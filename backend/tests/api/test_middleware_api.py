import pytest

from app.schemas.word import WordRead
from tests.factories import make_word_create_payload

pytestmark = pytest.mark.api


def test_post_lookup_returns_429_when_rate_limit_is_exceeded(client, monkeypatch) -> None:
    def fake_lookup_or_create_word(db, payload):  # noqa: ANN001
        return WordRead(
            id=1,
            source_word=payload.word,
            source_language="en",
            target_language="uk",
            slug="test-slug",
            transcription="[test]",
            primary_translation="тест",
            context_sentence="test sentence",
            origin="manual",
            created_at="2026-07-24T00:00:00Z",
            updated_at="2026-07-24T00:00:00Z",
            translation_options=[],
        )

    monkeypatch.setattr("app.routes.public.lookup_or_create_word", fake_lookup_or_create_word)

    for _ in range(3):
        response = client.post("/lookup", json={"word": "test", "direction": "en:uk"})
        assert response.status_code == 200

    response = client.post("/lookup", json={"word": "test", "direction": "en:uk"})

    assert response.status_code == 429
    assert response.json()["error_code"] == "rate_limit_exceeded"
    assert response.headers["Retry-After"]


def test_post_api_words_returns_413_for_too_large_request_body(client) -> None:
    payload = make_word_create_payload(context_sentence="A" * 120_000)

    response = client.post("/api/words", json=payload)

    assert response.status_code == 413
    assert response.json()["error_code"] == "request_too_large"
