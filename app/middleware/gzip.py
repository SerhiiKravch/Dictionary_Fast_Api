from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import Settings


def add_gzip_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        GZipMiddleware,
        minimum_size=settings.gzip_minimum_size,
    )
