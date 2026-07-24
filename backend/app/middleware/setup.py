from fastapi import FastAPI

from app.core.config import get_settings
from app.middleware.cors import add_cors_middleware
from app.middleware.gzip import add_gzip_middleware
from app.middleware.https_redirect import add_https_redirect_middleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.request_size import RequestSizeLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.trusted_host import add_trusted_host_middleware


def add_middlewares(app: FastAPI) -> None:
    settings = get_settings()

    add_https_redirect_middleware(app, settings)
    add_trusted_host_middleware(app, settings)
    add_cors_middleware(app, settings)
    add_gzip_middleware(app, settings)
    app.add_middleware(RequestSizeLimitMiddleware, settings=settings)
    app.add_middleware(RateLimitMiddleware, settings=settings)
    app.add_middleware(SecurityHeadersMiddleware, settings=settings)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(RequestLoggingMiddleware, settings=settings)
