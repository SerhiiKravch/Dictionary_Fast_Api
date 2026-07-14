from fastapi import FastAPI

from app.core.config import get_settings
from app.core.error_handlers import register_exception_handlers
from app.routes.api import router as api_router
from app.routes.pages import router as pages_router

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.app_debug)

register_exception_handlers(app)

app.include_router(pages_router)
app.include_router(api_router)
