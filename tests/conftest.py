"""Agent Factory — Test Configuration and Fixtures."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from src.config.settings import AppSettings, get_settings


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    """Clear the lru_cache before each test."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture()
def settings() -> AppSettings:
    """Return test settings instance."""
    return get_settings()


@pytest.fixture()
def client() -> TestClient:
    """Return a FastAPI test client."""
    from src.api.main import app
    return TestClient(app)
