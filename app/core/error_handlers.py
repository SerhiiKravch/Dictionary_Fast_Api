from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppError, IntegrationAppError, PersistenceAppError, ValidationAppError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationAppError)
    async def handle_validation_error(request: Request, exc: ValidationAppError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc) or "Validation error"},
        )

    @app.exception_handler(IntegrationAppError)
    async def handle_integration_error(request: Request, exc: IntegrationAppError) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={"detail": str(exc) or "External service error"},
        )

    @app.exception_handler(PersistenceAppError)
    async def handle_persistence_error(request: Request, exc: PersistenceAppError) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc) or "Database error"},
        )

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc) or "Application error"},
        )
