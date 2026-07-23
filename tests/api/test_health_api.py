import pytest

pytestmark = pytest.mark.api


def test_get_api_health(client) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
