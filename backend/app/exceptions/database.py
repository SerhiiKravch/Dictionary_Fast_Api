from app.exceptions import PersistenceAppError


class DatabaseError(PersistenceAppError):
    """Base error for database operations."""


class DatabaseConnectionError(DatabaseError):
    """Raised when the database is unavailable."""


class DatabaseIntegrityError(DatabaseError):
    """Raised when a DB integrity constraint is violated."""
