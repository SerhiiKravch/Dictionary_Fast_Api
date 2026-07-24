from fastapi import FastAPI

from app.core.config import get_settings
from app.middleware.cors import add_cors_middleware
from app.middleware.gzip import add_gzip_middleware
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware


def add_middlewares(app: FastAPI) -> None:
    settings = get_settings()

    add_cors_middleware(app, settings)
    add_gzip_middleware(app, settings)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
