from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.core.config import Settings


def add_https_redirect_middleware(app: FastAPI, settings: Settings) -> None:
    if settings.https_redirect_enabled:
        app.add_middleware(HTTPSRedirectMiddleware)
