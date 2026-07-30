from types import SimpleNamespace

import pytest

from app.exceptions.openai import OpenAIConfigurationError, OpenAIResponseFormatError
from app.models.enums import LanguageCode
from app.schemas.word import GeneratedWordPayload
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
    assert "Never include spaces in tags" in prompt
    assert "computer-science" in prompt


def test_openai_service_maps_validation_errors_to_response_format_error(monkeypatch) -> None:
    monkeypatch.setattr(
        openai_service,
        "get_settings",
        lambda: SimpleNamespace(
            openai_api_key="test-key",
            openai_model="gpt-4.1-mini",
        ),
    )

    class FakeResponses:
        def parse(self, **kwargs):
            GeneratedWordPayload.model_validate(
                {
                    "source_word": "run",
                    "source_language": "en",
                    "target_language": "uk",
                    "transcription": "[rʌn]",
                    "tags": ["computer!science"],
                    "translation_options": [],
                    "senses": [
                        {
                            "part_of_speech": "verb",
                            "primary_translation": "бігти",
                            "definition": "",
                            "position": 1,
                            "example_sentences": [
                                {
                                    "source_text": "I run every morning.",
                                    "translated_text": "Я бігаю щоранку.",
                                    "position": 1,
                                }
                            ],
                        }
                    ],
                }
            )
            raise AssertionError("ValidationError was expected before returning a response.")

    monkeypatch.setattr(
        openai_service,
        "OpenAI",
        lambda api_key: SimpleNamespace(responses=FakeResponses()),
    )

    service = openai_service.OpenAIService()

    with pytest.raises(OpenAIResponseFormatError):
        service.generate_word_payload("run", LanguageCode.ENGLISH, LanguageCode.UKRAINIAN)
