from app.exceptions import ValidationAppError


class InvalidDirectionError(ValidationAppError):
    """Raised when translation direction is invalid."""


class SameLanguageDirectionError(ValidationAppError):
    """Raised when source and target languages are the same."""


class EmptyWordError(ValidationAppError):
    """Raised when the input word is empty."""


class WordAlreadyExistsError(ValidationAppError):
    """Raised when a word already exists for the selected direction."""


class WordNotFoundError(ValidationAppError):
    """Raised when a word cannot be found."""
