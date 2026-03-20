.PHONY: help up down logs test lint format install check-env

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies with uv
	uv sync

check-env:
	@test -f .env || { echo "ERROR: Run: cp .env.example .env"; exit 1; }
	@test -f config.yaml || { echo "ERROR: Run: cp config.yaml.example config.yaml"; exit 1; }
	@echo "✅ Environment files OK"

up: check-env ## Start the full multi-agent stack
	docker compose up -d
	@echo "API: http://localhost:$${API_PORT:-8080}"
	@echo "Phoenix: http://localhost:6006"

up-infra: check-env ## Start infrastructure only (no app)
	docker compose up -d postgres redis weaviate phoenix

down:
	docker compose down

logs:
	docker compose logs -f

dev: check-env
	uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port $${API_PORT:-8080}

test:
	uv run pytest tests/ -v

test-unit:
	uv run pytest tests/unit/ -v

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

typecheck:
	uv run mypy src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
