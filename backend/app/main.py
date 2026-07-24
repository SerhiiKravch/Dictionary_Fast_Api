from fastapi import FastAPI

from app.core.config import get_settings
from app.core.error_handlers import register_exception_handlers
from app.middleware import add_middlewares
from app.routes.api import router as api_router
from app.routes.public import router as public_router

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.app_debug)

add_middlewares(app)
register_exception_handlers(app)

app.include_router(public_router)
app.include_router(api_router)
