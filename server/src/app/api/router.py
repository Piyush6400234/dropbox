from fastapi.routing import APIRouter

from src.app.api import monitoring
from src.app.api import core

api_router = APIRouter()

api_router.include_router(monitoring.router, prefix="/test", tags=["health_check"])
api_router.include_router(core.router, prefix="/core", tags=["core"])
