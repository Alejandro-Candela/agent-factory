"""Health check router."""
from __future__ import annotations
from fastapi import APIRouter
from src.config.settings import get_settings

router = APIRouter()

@router.get("/")
async def health_check() -> dict:
    settings = get_settings()
    return {"status": "healthy", "service": settings.project_name, "environment": settings.environment, "deployment_mode": settings.deployment_mode}

@router.get("/ready")
async def readiness_check() -> dict:
    return {"status": "ready"}
