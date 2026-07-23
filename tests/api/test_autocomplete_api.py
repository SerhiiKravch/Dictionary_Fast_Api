import pytest

from tests.factories import make_word_create_payload

pytestmark = pytest.mark.api


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
