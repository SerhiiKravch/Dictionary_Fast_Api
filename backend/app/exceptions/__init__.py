class AppError(Exception):
    """Base application exception."""


class ValidationAppError(AppError):
    """Base exception for validation/domain input errors."""


class IntegrationAppError(AppError):
    """Base exception for external integration errors."""


class PersistenceAppError(AppError):
    """Base exception for database/persistence errors."""
