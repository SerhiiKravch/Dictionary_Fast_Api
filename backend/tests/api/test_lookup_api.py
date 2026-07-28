import pytest

pytestmark = pytest.mark.api


def test_post_lookup_returns_422_for_invalid_direction(client) -> None:
    response = client.post("/lookup", json={"word": "test", "direction": "en-uk"})

    assert response.status_code == 422
    body = response.json()
    assert body["error_code"] == "request_validation_error"
    assert body["errors"]
