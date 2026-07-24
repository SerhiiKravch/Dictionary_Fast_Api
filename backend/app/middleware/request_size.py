from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.core.config import Settings


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings) -> None:
        super().__init__(app)
        self.settings = settings

    async def dispatch(self, request: Request, call_next) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None and int(content_length) > self.settings.request_max_body_size:
            return JSONResponse(
                status_code=413,
                content={
                    "detail": "Request body is too large.",
                    "error_code": "request_too_large",
                    "errors": [],
                },
            )

        return await call_next(request)
