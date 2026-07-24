import time
from collections import defaultdict, deque
from collections.abc import Callable
from threading import Lock

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.core.config import Settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings) -> None:
        super().__init__(app)
        self.settings = settings
        self._hits: defaultdict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def _build_key(self, request: Request) -> str:
        client_host = request.client.host if request.client else "unknown"
        return f"{client_host}:{request.method}:{request.url.path}"

    def _is_limited_path(self, path: str) -> bool:
        return path in self.settings.rate_limit_paths_list

    async def dispatch(self, request: Request, call_next: Callable[..., Response]) -> Response:
        if not self._is_limited_path(request.url.path):
            return await call_next(request)

        now = time.time()
        cutoff = now - self.settings.rate_limit_window_seconds
        key = self._build_key(request)

        with self._lock:
            hits = self._hits[key]
            while hits and hits[0] <= cutoff:
                hits.popleft()

            if len(hits) >= self.settings.rate_limit_max_requests:
                retry_after = max(1, int(hits[0] + self.settings.rate_limit_window_seconds - now))
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded.",
                        "error_code": "rate_limit_exceeded",
                        "errors": [],
                    },
                    headers={"Retry-After": str(retry_after)},
                )

            hits.append(now)

        return await call_next(request)
