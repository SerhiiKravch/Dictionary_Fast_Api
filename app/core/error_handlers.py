from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import AppError, IntegrationAppError, PersistenceAppError, ValidationAppError
from app.exceptions.database import DatabaseConnectionError
from app.exceptions.dictionary import WordAlreadyExistsError, WordNotFoundError
from app.exceptions.openai import (
    OpenAIRateLimitError,
    OpenAIResponseFormatError,
    OpenAIUnavailableError,
)


def build_error_response(
    *,
    status_code: int,
    detail: str,
    error_code: str,
    errors: list[dict[str, object]] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
            "error_code": error_code,
            "errors": errors or [],
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return build_error_response(
            status_code=422,
            detail="Request validation failed.",
            error_code="request_validation_error",
            errors=[dict(error) for error in exc.errors()],
        )

    @app.exception_handler(WordAlreadyExistsError)
    async def handle_word_exists_error(
        request: Request,
        exc: WordAlreadyExistsError,
    ) -> JSONResponse:
        return build_error_response(
            status_code=409,
            detail=str(exc) or "Word already exists.",
            error_code="word_already_exists",
        )

    @app.exception_handler(WordNotFoundError)
    async def handle_word_not_found_error(
        request: Request,
        exc: WordNotFoundError,
    ) -> JSONResponse:
        return build_error_response(
            status_code=404,
            detail=str(exc) or "Word not found.",
            error_code="word_not_found",
        )

    @app.exception_handler(OpenAIRateLimitError)
    async def handle_openai_rate_limit_error(
        request: Request,
        exc: OpenAIRateLimitError,
    ) -> JSONResponse:
        return build_error_response(
            status_code=429,
            detail=str(exc) or "OpenAI rate limit exceeded.",
            error_code="openai_rate_limit",
        )

    @app.exception_handler(OpenAIUnavailableError)
    async def handle_openai_unavailable_error(
        request: Request,
        exc: OpenAIUnavailableError,
    ) -> JSONResponse:
        return build_error_response(
            status_code=503,
            detail=str(exc) or "OpenAI service is unavailable.",
            error_code="openai_unavailable",
        )

    @app.exception_handler(OpenAIResponseFormatError)
    async def handle_openai_response_format_error(
        request: Request,
        exc: OpenAIResponseFormatError,
    ) -> JSONResponse:
        return build_error_response(
            status_code=502,
            detail=str(exc) or "OpenAI returned an invalid response format.",
            error_code="openai_response_format_error",
        )

    @app.exception_handler(DatabaseConnectionError)
    async def handle_database_connection_error(
        request: Request,
        exc: DatabaseConnectionError,
    ) -> JSONResponse:
        return build_error_response(
            status_code=503,
            detail=str(exc) or "Database connection is unavailable.",
            error_code="database_connection_error",
        )

    @app.exception_handler(ValidationAppError)
    async def handle_validation_error(request: Request, exc: ValidationAppError) -> JSONResponse:
        return build_error_response(
            status_code=400,
            detail=str(exc) or "Validation error.",
            error_code="validation_error",
        )

    @app.exception_handler(IntegrationAppError)
    async def handle_integration_error(request: Request, exc: IntegrationAppError) -> JSONResponse:
        return build_error_response(
            status_code=502,
            detail=str(exc) or "External service error.",
            error_code="integration_error",
        )

    @app.exception_handler(PersistenceAppError)
    async def handle_persistence_error(request: Request, exc: PersistenceAppError) -> JSONResponse:
        return build_error_response(
            status_code=500,
            detail=str(exc) or "Database error.",
            error_code="persistence_error",
        )

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return build_error_response(
            status_code=500,
            detail=str(exc) or "Application error.",
            error_code="application_error",
        )
