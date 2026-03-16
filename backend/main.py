from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api_routes import router
from backend.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
