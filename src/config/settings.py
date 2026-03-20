"""
Agent Factory — Pydantic Settings
Multi-model inference (supervisor + worker) with module toggles.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Root application settings — loaded from .env."""

    project_name: str = "agent-factory"
    environment: Literal["development", "staging", "production"] = "development"
    deployment_mode: Literal["poc", "production"] = "poc"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # Module toggles
    module_inference: bool = True
    module_vector_db: bool = True
    module_orchestration: bool = True
    module_guardrails: bool = False
    module_observability: bool = False
    module_frontend: bool = False
    module_hitl: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8080
    api_workers: int = 4
    api_cors_origins: str = "http://localhost:3001"

    # Database
    database_url: SecretStr = Field(default=SecretStr("postgresql://postgres:postgres@localhost:5432/agent_factory_db"))

    # Supervisor model
    supervisor_model_provider: str = "ollama"
    supervisor_model: str = "qwen3:7b"
    supervisor_temperature: float = 1.0

    # Worker model
    worker_model_provider: str = "ollama"
    worker_model: str = "qwen3:4b"
    worker_temperature: float = 0.1

    # OpenAI (production)
    openai_api_key: SecretStr = Field(default=SecretStr(""))
    anthropic_api_key: SecretStr = Field(default=SecretStr(""))

    # HITL
    hitl_enabled: bool = False
    hitl_timeout_seconds: int = 300

    # Agents
    max_agent_roles: int = 10
    agent_debate_rounds: int = 2

    # OTel
    otel_enabled: bool = False
    otel_service_name: str = "agent-factory"
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("api_cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> list[str]:
        """Convert comma-separated origins string to list."""
        return [origin.strip() for origin in v.split(",")]

    @property
    def cors_origins(self) -> list[str]:
        """Return parsed CORS origins."""
        return self.parse_cors_origins(self.api_cors_origins)


def load_yaml_config(path: Path = Path("config.yaml")) -> dict:
    """Load the config.yaml file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found at {path}. "
            "Run: cp config.yaml.example config.yaml"
        )
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return cached application settings."""
    return AppSettings()
