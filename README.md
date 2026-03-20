# 🏭 Agent Factory

> **Golden Stack #4** — Multi-Agent Orchestration with Human-in-the-Loop

This blueprint enables **multi-agent workflows** where specialised agents reason, debate, and iterate to produce validated, high-quality outputs. Designed for complex tasks requiring multiple perspectives: legal review, incident triage, logistics planning.

---

## 🏗️ Architecture

```
  Task Input
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│              SUPERVISOR AGENT (o3-mini)                  │
│  • Decomposes task into subtasks                         │
│  • Assigns subtasks to specialist agents                 │
│  • Aggregates and validates final output                 │
└──────┬──────────────────────────────────────────────────┘
       │ spawn
       ├──────────────────────────────────────┐
       │                                      │
┌──────▼──────┐      ┌──────────────┐   ┌────▼────────┐
│  RESEARCHER  │      │    CRITIC    │   │   WRITER    │
│ (worker LLM) │      │ (worker LLM) │   │(worker LLM) │
│              │      │              │   │             │
│ Vector search│      │ Reviews and  │   │ Produces    │
│ Web search   │      │ challenges   │   │ structured  │
│ RAG pipeline │ ────▶│ outputs      │──▶│ final output│
└──────────────┘      └──────────────┘   └─────────────┘
                                               │
                            ┌──────────────────┘
                            │ HITL Gate
                            ▼
                    ┌───────────────┐      ✅ Approve
                    │ Human Review  │ ──────────────────▶ Done
                    │  Dashboard    │      ❌ Reject
                    └───────────────┘ ──────────────────▶ Retry
                    (Next.js + WebSocket)
```

---

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose v2.x
- OpenAI API key (for o3-mini supervisor)
- `uv` package manager

### 1. Configure
```bash
cp .env.example .env
cp config.yaml.example config.yaml
nano .env   # Set OPENAI_API_KEY, PINECONE_API_KEY, etc.
```

### 2. Start
```bash
make up
# Phoenix UI: http://localhost:6006
# Agent API:  http://localhost:8080
```

---

## ⚙️ Key Configuration

### Agent Role Customisation (`config.yaml`)
```yaml
agents:
  debate_rounds: 3             # How many critic-writer iterations

  roles:
    - id: supervisor
      model_override:
        model: o3-mini          # Heavy reasoning model
        reasoning_effort: high

    - id: researcher
      tools:
        - vector_search
        - web_search

  hitl:
    enabled: true
    approval_required_at:
      - "supervisor:task_plan_ready"
      - "writer:draft_complete"
    timeout_action: reject       # reject | auto_approve
```

### Switching Vector DB (`config.yaml`)
```yaml
vector_db:
  provider: pinecone             # pinecone | weaviate

  pinecone:
    spec:
      serverless:
        cloud: gcp
        region: us-central1
    multi_tenancy:
      enabled: true              # One namespace per client
```

---

## 🛡️ Guardrails AI

All agent outputs pass through Guardrails AI validators before being returned:

```yaml
security:
  guardrails:
    validation_mode: strict
    on_fail: reask               # Agent retries if output fails validation
    validators:
      - guardrails/nsfw_text
      - guardrails/detect_pii
      - guardrails/valid_json
```

---

## 📊 Observability

| Tool | URL | Notes |
|---|---|---|
| Arize Phoenix | `http://localhost:6006` | OSS — self-hosted, zero cost |
| LangSmith | LangSmith cloud dashboard | Set `LANGCHAIN_API_KEY` |

Switch via `OBSERVABILITY_BACKEND` in `.env`.

---

## 🧪 Testing

```bash
make test-unit   # Unit tests (no external services)
make test        # Full test suite (requires Docker stack)
```

---

## 📄 License
Proprietary — All rights reserved.
