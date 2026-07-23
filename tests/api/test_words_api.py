import pytest

from tests.factories import make_word_create_payload

pytestmark = pytest.mark.api


def test_get_api_words_returns_list(client) -> None:
    response = client.get("/api/words")

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total": 0,
        "limit": 20,
        "offset": 0,
    }


def test_get_api_words_returns_paginated_response(client) -> None:
    client.post("/api/words", json=make_word_create_payload(source_word="apple"))

    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="banana",
            primary_translation="банан",
            context_sentence="I ate a banana.",
        ),
    )

    response = client.get("/api/words?limit=1&offset=0")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["limit"] == 1
    assert body["offset"] == 0
    assert len(body["items"]) == 1
    assert [item["source_word"] for item in body["items"]] == ["banana"]


def test_get_api_words_returns_paginated_response_with_offset(client) -> None:
    client.post("/api/words", json=make_word_create_payload(source_word="apple"))

    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="banana",
            primary_translation="банан",
            context_sentence="I ate a banana.",
        ),
    )

    client.post("/api/words", json=make_word_create_payload(source_word="phone"))

    client.post("/api/words", json=make_word_create_payload(source_word="cavoon"))

    response = client.get("/api/words?limit=2&offset=1")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 4
    assert body["limit"] == 2
    assert body["offset"] == 1
    assert len(body["items"]) == 2
    assert [item["source_word"] for item in body["items"]] == ["phone", "banana"]


def test_get_api_words_returns_empty_page(client) -> None:
    response = client.get("/api/words?limit=10&offset=100")

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total": 0,
        "limit": 10,
        "offset": 100,
    }


def test_get_api_words_filters_by_source_language(client) -> None:
    client.post("/api/words", json=make_word_create_payload(source_word="apple"))
    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="кіт",
            source_language="uk",
            target_language="en",
            primary_translation="cat",
            context_sentence="Це кіт.",
        ),
    )

    response = client.get("/api/words?source_language=uk")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert [item["source_word"] for item in body["items"]] == ["кіт"]


def test_get_api_words_filters_by_origin(client) -> None:
    client.post("/api/words", json=make_word_create_payload(source_word="apple"))
    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="banana",
            primary_translation="банан",
            context_sentence="I ate a banana.",
            origin="imported",
        ),
    )

    response = client.get("/api/words?origin=imported")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert [item["source_word"] for item in body["items"]] == ["banana"]


def test_get_api_words_filters_by_search(client) -> None:
    client.post("/api/words", json=make_word_create_payload(source_word="apple"))
    client.post("/api/words", json=make_word_create_payload(source_word="banana"))
    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="pineapple",
            primary_translation="ананас",
            context_sentence="Pineapple is sweet.",
        ),
    )

    response = client.get("/api/words?search=apple")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert [item["source_word"] for item in body["items"]] == ["pineapple", "apple"]


def test_get_api_words_combines_filters_and_pagination(client) -> None:
    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="apple",
            origin="manual",
        ),
    )
    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="pineapple",
            primary_translation="ананас",
            context_sentence="Pineapple is sweet.",
            origin="manual",
        ),
    )
    client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="application",
            primary_translation="застосунок",
            context_sentence="The application is ready.",
            origin="imported",
        ),
    )

    response = client.get(
        "/api/words?source_language=en&target_language=uk&origin=manual&search=apple"
        "&limit=1&offset=0"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["limit"] == 1
    assert body["offset"] == 0
    assert [item["source_word"] for item in body["items"]] == ["pineapple"]


def test_post_api_words_creates_word(client) -> None:
    payload = make_word_create_payload()

    response = client.post("/api/words", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["source_word"] == "apple"
    assert body["slug"].startswith("apple-en-uk")


def test_post_api_words_returns_409_for_duplicate(client) -> None:
    payload = make_word_create_payload()
    client.post("/api/words", json=payload)

    response = client.post("/api/words", json=payload)

    assert response.status_code == 409
    assert response.json()["error_code"] == "word_already_exists"


def test_post_api_words_returns_422_for_invalid_body(client) -> None:
    response = client.post("/api/words", json={"source_word": "apple"})

    assert response.status_code == 422
    assert response.json()["error_code"] == "request_validation_error"


def test_get_word_by_slug_returns_404_for_missing_word(client) -> None:
    response = client.get("/word/missing-slug")

    assert response.status_code == 404
    assert response.json()["error_code"] == "word_not_found"


def test_get_api_word_by_slug_returns_word(client) -> None:
    create_response = client.post("/api/words", json=make_word_create_payload())
    slug = create_response.json()["slug"]

    response = client.get(f"/api/words/{slug}")

    assert response.status_code == 200
    body = response.json()
    assert body["slug"] == slug
    assert body["source_word"] == "apple"


def test_get_api_word_by_slug_returns_404_for_missing_word(client) -> None:
    response = client.get("/api/words/missing-slug")

    assert response.status_code == 404
    assert response.json()["error_code"] == "word_not_found"
