from types import SimpleNamespace

import pytest

from app.exceptions.openai import OpenAIConfigurationError
from app.services import openai_service


def test_openai_service_raises_configuration_error_when_api_key_missing(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        openai_service,
        "get_settings",
        lambda: SimpleNamespace(
            openai_api_key="",
            openai_model="gpt-4.1-mini",
        ),
    )

    with pytest.raises(OpenAIConfigurationError):
        openai_service.OpenAIService()
