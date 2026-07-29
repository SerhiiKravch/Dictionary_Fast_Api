import pytest

from tests.factories import make_word_create_payload, make_word_relation_payload

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


def test_get_api_words_uses_gzip_for_large_response(client) -> None:
    for index in range(4):
        client.post(
            "/api/words",
            json=make_word_create_payload(
                source_word=f"word-{index}",
                primary_translation=f"переклад-{index}",
                context_sentence="A" * 300,
            ),
        )

    response = client.get("/api/words", headers={"Accept-Encoding": "gzip"})

    assert response.status_code == 200
    assert response.headers["content-encoding"] == "gzip"


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
    assert body["senses"][0]["primary_translation"] == "яблуко"
    assert body["senses"][0]["example_sentences"][0]["source_text"] == "I ate an apple."


def test_post_api_words_creates_word_with_metadata(client) -> None:
    payload = make_word_create_payload(
        source_word="run",
        primary_translation="бігти",
        context_sentence="I run every morning.",
        difficulty_level="a2",
        tags=["spoken", "common"],
        inflections=[
            {"form_type": "past_simple", "value": "ran", "notes": ""},
            {"form_type": "past_participle", "value": "run", "notes": "irregular"},
        ],
    )

    response = client.post("/api/words", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["difficulty_level"] == "a2"
    assert [tag["name"] for tag in body["tags"]] == ["common", "spoken"]
    assert [(item["form_type"], item["value"]) for item in body["inflections"]] == [
        ("past_simple", "ran"),
        ("past_participle", "run"),
    ]
    assert body["senses"][0]["part_of_speech"] == "other"


def test_post_api_words_creates_word_with_senses_payload(client) -> None:
    response = client.post(
        "/api/words",
        json=make_word_create_payload(
            primary_translation=None,
            context_sentence=None,
            senses=[
                {
                    "part_of_speech": "verb",
                    "primary_translation": "бігти",
                    "definition": "to move quickly on foot",
                    "position": 1,
                    "example_sentences": [
                        {
                            "source_text": "I run every morning.",
                            "translated_text": "Я бігаю щоранку.",
                            "position": 1,
                        }
                    ],
                },
                {
                    "part_of_speech": "noun",
                    "primary_translation": "пробіжка",
                    "definition": "an act of running",
                    "position": 2,
                    "example_sentences": [
                        {
                            "source_text": "She went for a run.",
                            "translated_text": "Вона пішла на пробіжку.",
                            "position": 1,
                        }
                    ],
                },
            ],
        ),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["primary_translation"] == "бігти"
    assert body["context_sentence"] == "I run every morning."
    assert len(body["senses"]) == 2
    assert body["senses"][1]["primary_translation"] == "пробіжка"


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


def test_post_api_words_returns_422_when_legacy_and_senses_are_missing(client) -> None:
    response = client.post(
        "/api/words",
        json=make_word_create_payload(
            primary_translation=None,
            context_sentence=None,
            senses=[],
        ),
    )

    assert response.status_code == 422
    assert response.json()["error_code"] == "request_validation_error"


def test_post_api_words_returns_422_for_invalid_tag(client) -> None:
    response = client.post(
        "/api/words",
        json=make_word_create_payload(tags=["spoken word"]),
    )

    assert response.status_code == 422
    body = response.json()
    assert body["error_code"] == "request_validation_error"
    assert any("Tag may contain only letters" in error["msg"] for error in body["errors"])


def test_post_api_words_returns_422_for_duplicate_inflection_types(client) -> None:
    response = client.post(
        "/api/words",
        json=make_word_create_payload(
            inflections=[
                {"form_type": "past_simple", "value": "ran", "notes": ""},
                {"form_type": "past_simple", "value": "run", "notes": ""},
            ]
        ),
    )

    assert response.status_code == 422
    body = response.json()
    assert body["error_code"] == "request_validation_error"
    assert any("Duplicate inflection types" in error["msg"] for error in body["errors"])


def test_post_api_words_returns_422_for_invalid_inflection_enum(client) -> None:
    response = client.post(
        "/api/words",
        json=make_word_create_payload(
            inflections=[
                {"form_type": "future_simple", "value": "will run", "notes": ""},
            ]
        ),
    )

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
    assert body["senses"][0]["primary_translation"] == "яблуко"


def test_get_api_word_by_slug_returns_metadata(client) -> None:
    create_response = client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="run",
            primary_translation="бігти",
            context_sentence="I run every morning.",
            difficulty_level="a2",
            tags=["spoken", "common"],
            inflections=[
                {"form_type": "past_simple", "value": "ran", "notes": ""},
            ],
        ),
    )
    slug = create_response.json()["slug"]

    response = client.get(f"/api/words/{slug}")

    assert response.status_code == 200
    body = response.json()
    assert body["difficulty_level"] == "a2"
    assert [tag["name"] for tag in body["tags"]] == ["common", "spoken"]
    assert body["inflections"] == [
        {"id": 1, "form_type": "past_simple", "value": "ran", "notes": ""}
    ]
    assert body["senses"][0]["example_sentences"][0]["source_text"] == "I run every morning."


def test_get_api_word_by_slug_returns_404_for_missing_word(client) -> None:
    response = client.get("/api/words/missing-slug")

    assert response.status_code == 404
    assert response.json()["error_code"] == "word_not_found"


def test_post_api_word_relation_creates_related_link(client) -> None:
    first = client.post("/api/words", json=make_word_create_payload(source_word="apple")).json()
    second = client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="fruit",
            primary_translation="фрукт",
            context_sentence="Fruit is healthy.",
        ),
    ).json()

    response = client.post(
        f"/api/words/{first['id']}/relations",
        json=make_word_relation_payload(
            target_word_id=second["id"],
            relation_type="related",
            notes="semantic neighbor",
        ),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["relation_type"] == "related"
    assert body["notes"] == "semantic neighbor"
    assert body["related_word"]["id"] == second["id"]
    assert body["related_word"]["source_word"] == "fruit"


def test_post_api_word_relation_rejects_self_relation(client) -> None:
    word = client.post("/api/words", json=make_word_create_payload(source_word="apple")).json()

    response = client.post(
        f"/api/words/{word['id']}/relations",
        json=make_word_relation_payload(target_word_id=word["id"]),
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "invalid_word_relation"


def test_post_api_word_relation_rejects_duplicate_relation(client) -> None:
    first = client.post("/api/words", json=make_word_create_payload(source_word="apple")).json()
    second = client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="fruit",
            primary_translation="фрукт",
            context_sentence="Fruit is healthy.",
        ),
    ).json()

    payload = make_word_relation_payload(target_word_id=second["id"], relation_type="related")
    client.post(f"/api/words/{first['id']}/relations", json=payload)
    response = client.post(f"/api/words/{first['id']}/relations", json=payload)

    assert response.status_code == 409
    assert response.json()["error_code"] == "word_relation_already_exists"


def test_get_api_word_relations_returns_bidirectional_synonym(client) -> None:
    first = client.post("/api/words", json=make_word_create_payload(source_word="big")).json()
    second = client.post(
        "/api/words",
        json=make_word_create_payload(
            source_word="large",
            primary_translation="великий",
            context_sentence="A large house.",
        ),
    ).json()

    create_response = client.post(
        f"/api/words/{first['id']}/relations",
        json=make_word_relation_payload(target_word_id=second["id"], relation_type="synonym"),
    )
    assert create_response.status_code == 201

    first_relations = client.get(f"/api/words/{first['slug']}/relations")
    second_relations = client.get(f"/api/words/{second['slug']}/relations")

    assert first_relations.status_code == 200
    assert second_relations.status_code == 200
    assert first_relations.json()["items"][0]["related_word"]["id"] == second["id"]
    assert second_relations.json()["items"][0]["related_word"]["id"] == first["id"]
