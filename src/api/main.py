"""
Agent Factory — FastAPI Application Entrypoint
Multi-agent orchestration with HITL gates and WebSocket support.
"""
from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config.settings import get_settings
from src.utils.logging import get_logger, setup_telemetry

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    settings = get_settings()
    logger.info(
        "Starting Agent Factory API",
        extra={
            "environment": settings.environment,
            "deployment_mode": settings.deployment_mode,
            "hitl_enabled": settings.module_hitl,
            "max_roles": settings.max_agent_roles,
        },
    )
    if settings.module_observability:
        setup_telemetry(settings)
    yield
    logger.info("Shutting down Agent Factory API")


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title="Agent Factory API",
        description="Multi-agent orchestration factory with HITL. "
        f"Mode: {settings.deployment_mode}",
        version="2.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}s"
        return response

    from src.api.routers import agent, health
    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(agent.router, prefix="/api/v1/agent", tags=["Agent"])

    return app


class TaskRequest(BaseModel):
    """Incoming task request for multi-agent processing."""
    task: str
    thread_id: str | None = None
    require_approval: bool = False


class TaskResponse(BaseModel):
    """Task response with agent execution trail."""
    result: str
    thread_id: str
    agent_trail: list[dict] = []
    pending_approval: bool = False
    trace_id: str | None = None


app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        log_level=settings.log_level.lower(),
        reload=(settings.environment == "development"),
    )
