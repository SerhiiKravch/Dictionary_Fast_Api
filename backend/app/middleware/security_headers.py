from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import Settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings) -> None:
        super().__init__(app)
        self.settings = settings

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Frame-Options"] = self.settings.security_frame_options
        response.headers["X-Content-Type-Options"] = self.settings.security_content_type_options
        response.headers["Referrer-Policy"] = self.settings.security_referrer_policy
        return response
