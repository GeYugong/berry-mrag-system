from fastapi import FastAPI

from backend.api_routes import router
from backend.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)
app.include_router(router)
