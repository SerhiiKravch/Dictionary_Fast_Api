from tests.factories import make_word_create_payload


def test_get_api_health(client) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_api_words_returns_list(client) -> None:
    response = client.get("/api/words")

    assert response.status_code == 200
    assert response.json() == []


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
