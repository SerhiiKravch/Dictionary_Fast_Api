"""Pydantic schemas package."""

from app.schemas.common import ErrorResponse, HealthResponse, MessageResponse
from app.schemas.word import (
    AutocompleteItem,
    AutocompleteResponse,
    GeneratedTranslationOption,
    GeneratedWordPayload,
    WordLookupRequest,
)

__all__ = [
    "ErrorResponse",
    "HealthResponse",
    "MessageResponse",
    "AutocompleteItem",
    "AutocompleteResponse",
    "GeneratedTranslationOption",
    "GeneratedWordPayload",
    "WordLookupRequest",
]
