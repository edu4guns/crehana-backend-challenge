from fastapi import APIRouter

from app.infrastructure.config import get_settings


router = APIRouter()


@router.get("/healthz", tags=["health"])
def healthcheck() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
    }

