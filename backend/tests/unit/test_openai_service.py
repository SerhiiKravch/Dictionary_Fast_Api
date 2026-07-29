from types import SimpleNamespace

import pytest

from app.exceptions.openai import OpenAIConfigurationError
from app.models.enums import LanguageCode
from app.services import openai_service

pytestmark = pytest.mark.unit


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


def test_openai_service_build_prompt_requests_senses_structure(monkeypatch) -> None:
    monkeypatch.setattr(
        openai_service,
        "get_settings",
        lambda: SimpleNamespace(
            openai_api_key="test-key",
            openai_model="gpt-4.1-mini",
        ),
    )
    monkeypatch.setattr(openai_service, "OpenAI", lambda api_key: SimpleNamespace())

    service = openai_service.OpenAIService()

    prompt = service.build_prompt("run", LanguageCode.ENGLISH, LanguageCode.UKRAINIAN)

    assert "senses array" in prompt
    assert "example_sentences" in prompt
    assert "primary_translation and context_sentence" in prompt
