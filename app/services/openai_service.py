from openai import APIError, OpenAI, OpenAIError, RateLimitError

from app.core.config import get_settings
from app.exceptions.openai import (
    OpenAIConfigurationError,
    OpenAIRateLimitError,
    OpenAIResponseFormatError,
    OpenAIUnavailableError,
)
from app.models.enums import LanguageCode
from app.schemas.word import GeneratedWordPayload


class OpenAIService:
    def __init__(self) -> None:
        settings = get_settings()
        api_key = settings.openai_api_key.strip()
        if not api_key:
            raise OpenAIConfigurationError("OpenAI API key is not configured.")

        try:
            self.client = OpenAI(api_key=api_key)
        except OpenAIError as exc:
            raise OpenAIConfigurationError("OpenAI client configuration is invalid.") from exc

        self.model = settings.openai_model

    def build_prompt(
        self,
        word: str,
        source_language: LanguageCode,
        target_language: LanguageCode,
    ) -> str:
        return (
            f"Generate dictionary data for '{word}' from "
            f"{source_language.value} to {target_language.value}. "
            "Return valid JSON."
        )

    def generate_word_payload(
        self,
        word: str,
        source_language: LanguageCode,
        target_language: LanguageCode,
    ) -> GeneratedWordPayload:
        prompt = self.build_prompt(word, source_language, target_language)

        try:
            response = self.client.responses.parse(
                model=self.model,
                input=prompt,
                text_format=GeneratedWordPayload,
            )
        except RateLimitError as exc:
            raise OpenAIRateLimitError("OpenAI rate limit exceeded.") from exc
        except APIError as exc:
            raise OpenAIUnavailableError("OpenAI API request failed.") from exc
        except OpenAIError as exc:
            raise OpenAIUnavailableError("OpenAI client request failed.") from exc

        if response.output_parsed is None:
            raise OpenAIResponseFormatError("OpenAI returned an invalid structured response.")

        return response.output_parsed
