from tests.factories import make_word_create_payload


def test_get_api_health(client) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


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


def test_get_api_autocomplete_returns_empty_without_query(client) -> None:
    response = client.get("/api/autocomplete")

    assert response.status_code == 200
    assert response.json() == {"results": []}


def test_get_api_autocomplete_returns_matches_for_prefix(client) -> None:
    client.post("/api/words", json=make_word_create_payload(source_word="apple"))
    client.post("/api/words", json=make_word_create_payload(source_word="apricot"))
    client.post("/api/words", json=make_word_create_payload(source_word="banana"))

    response = client.get("/api/autocomplete?q=ap")

    assert response.status_code == 200
    assert response.json() == {"results": ["apple", "apricot"]}


def test_get_api_autocomplete_limits_results_to_ten(client) -> None:
    for index in range(12):
        client.post(
            "/api/words",
            json=make_word_create_payload(
                source_word=f"app{index}",
                primary_translation=f"переклад-{index}",
                context_sentence=f"Sentence {index}",
            ),
        )

    response = client.get("/api/autocomplete?q=app")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 10


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
