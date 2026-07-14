from app.exceptions import IntegrationAppError


class OpenAIServiceError(IntegrationAppError):
    """Base error for OpenAI integration."""


class OpenAIRateLimitError(OpenAIServiceError):
    """Raised when the OpenAI API rate limit is hit."""


class OpenAIResponseFormatError(OpenAIServiceError):
    """Raised when the model response cannot be parsed or validated."""


class OpenAIUnavailableError(OpenAIServiceError):
    """Raised when the OpenAI API is temporarily unavailable."""
