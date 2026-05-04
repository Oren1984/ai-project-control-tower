# API Keys and Environment Variables Guide

## 1. Purpose

This document is the single reference for all environment variables in the AI Project Control Tower.
It tells you exactly where each variable is defined, where it is loaded, and where it is consumed —
so you never have to grep the whole project to find an env-related setting.

---

## 2. Quick Start

```bash
# 1. Copy the example file (never commit the real .env)
cp .env.example .env

# 2. Open .env and set the two required variables
#    HOST_REPOS_PATH  — the host directory mounted into containers as /workspace
#    ALLOWED_SCAN_PATHS — scanner allowlist (see Section 4)

# 3. Optionally add an LLM key (agents run in stub mode without one)
#    OPENAI_API_KEY=sk-...
#    ANTHROPIC_API_KEY=sk-ant-...

# 4. Start the stack
docker compose up
```

> **Never commit `.env`.**  
> Only `.env.example` (with placeholder values) is tracked by Git.

---

## 3. Main Environment Files

| File | Purpose | Notes |
|---|---|---|
| `.env.example` | Template with all supported variables | Committed to Git; fill and copy to `.env` |
| `.env` | Actual runtime values | **Not committed** — already ignored by `.gitignore` (line 2) |
| `docker-compose.yml` | Declares which variables each service consumes | Uses `${VAR:-default}` syntax; reads `.env` via `env_file` on the `api` service |
| `app/core/config.py` | Pydantic `Settings` class — sole config loader for the backend | Reads from `.env` and environment variables; validates and provides defaults |
| `ui/services/api_client.py` | Reads `API_BASE_URL` and `DEMO_MODE` for the Streamlit frontend | Falls back to `localhost` defaults if vars are absent |
| `ui/main.py` | Reads `DEMO_MODE` to seed Streamlit session state | Line 61 |
| `ui/pages/page_settings.py` | Reads `API_BASE_URL` for the Settings page default | Line 14 |
| `.streamlit/config.toml` | Streamlit server configuration (headless, no usage stats) | No secrets here; UI-only settings |

---

## 4. API Keys Map

| Variable | Required | Purpose | Feature | Where to Set | Where Loaded | Where Used | Line / Area |
|---|---|---|---|---|---|---|---|
| `HOST_REPOS_PATH` | **Required** (Docker) | Host directory mounted as `/workspace` inside containers | Repository scanner | `.env` | `docker-compose.yml` (volume bind) | `docker-compose.yml` line 39 | compose `api` volumes section |
| `ALLOWED_SCAN_PATHS` | **Required** | Comma-sep or JSON list of container paths the scanner may read | Security allowlist | `.env` | `app/core/config.py` lines 93–94 | `app/scanner/path_validator.py` lines 3, 18 | scanner security check |
| `DATABASE_URL` | **Required** | Full SQLAlchemy connection string for PostgreSQL + pgvector | All DB operations | `.env` | `app/core/config.py` lines 88–91 | `app/db/session.py` line 5 | engine creation |
| `POSTGRES_USER` | **Required** (Docker) | PostgreSQL username | Database container init + `DATABASE_URL` construction | `.env` | `docker-compose.yml` `db` service env + `api` service `DATABASE_URL` | `docker-compose.yml` lines 5, 25 | compose `db` + `api` services |
| `POSTGRES_PASSWORD` | **Required** (Docker) | PostgreSQL password | Database container init + `DATABASE_URL` construction | `.env` | `docker-compose.yml` | `docker-compose.yml` lines 6, 25 | compose `db` + `api` services |
| `POSTGRES_DB` | **Required** (Docker) | PostgreSQL database name | Database container init + `DATABASE_URL` construction | `.env` | `docker-compose.yml` | `docker-compose.yml` lines 7, 25 | compose `db` + `api` services |
| `API_BASE_URL` | Optional | Backend API base URL used by the Streamlit UI | UI → API communication | `.env` or container env | `ui/services/api_client.py` line 8; `ui/pages/page_settings.py` line 14 | All UI pages (via `api_client._get/_post`) | default: `http://localhost:8013/api/v1` (local) / `http://api:8000/api/v1` (Docker) |
| `DEMO_MODE` | Optional | Start UI in demo mode; serves canned data without a live backend | Demo / presentation mode | `.env` | `ui/main.py` line 61; `ui/services/api_client.py` line 24 | All UI pages — bypasses real API calls | default: `false` |
| `APP_NAME` | Optional | Application display name | FastAPI title + startup log | `.env` | `app/core/config.py` line 83 | `app/main.py` lines 21, 27 | default: `AI Project Control Tower` |
| `APP_VERSION` | Optional | Application version string | FastAPI OpenAPI docs + startup log | `.env` | `app/core/config.py` line 84 | `app/main.py` lines 21, 28 | default: `0.1.0` |
| `LOG_LEVEL` | Optional | structlog minimum level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | Logging | `.env` | `app/core/config.py` line 86 | `app/main.py` line 15 | default: `INFO` |
| `DEBUG` | Optional | Enable FastAPI debug mode | Development only | `.env` | `app/core/config.py` line 85 | `app/main.py` (FastAPI init) | default: `false` |
| `MAX_SCAN_FILE_SIZE_BYTES` | Optional | Maximum bytes per file the scanner will read | Scanner resource limit | `.env` | `app/core/config.py` line 95 | `app/scanner/` (file reading) | default: `1048576` (1 MB) |
| `CORS_ALLOWED_ORIGINS` | Optional | Comma-sep or JSON list of origins allowed to call the API | CORS middleware | `.env` | `app/core/config.py` lines 97–103 | `app/main.py` line 34 | default: `localhost:8513`, `localhost:3012`, `ui:8501` |
| `GRAFANA_ADMIN_PASSWORD` | Optional | Grafana web UI admin password | Observability dashboards | `.env` | `docker-compose.yml` line 79 (`GF_SECURITY_ADMIN_PASSWORD`) | Grafana container | default: `admin` — **change in production** |
| `OPENAI_API_KEY` | Optional / planned | Optional provider key for future LLM-backed analysis. No code in `app/` reads this variable today. The current system operates in deterministic stub mode when no provider integration is enabled. | AI agents (future) | `.env` | Not loaded by any current code — commented placeholder in `.env.example` only | Not used by current code | — |
| `ANTHROPIC_API_KEY` | Optional / planned | Optional provider key for future LLM-backed analysis. No code in `app/` reads this variable today. The current system operates in deterministic stub mode when no provider integration is enabled. | AI agents (future) | `.env` | Not loaded by any current code — commented placeholder in `.env.example` only | Not used by current code | — |

---

## 5. Provider-Specific Setup

### PostgreSQL + pgvector

| Variable | Placeholder Example |
|---|---|
| `DATABASE_URL` | `postgresql://control_tower:control_tower_pass@localhost:5432/control_tower_db` |
| `POSTGRES_USER` | `control_tower` |
| `POSTGRES_PASSWORD` | `control_tower_pass` |
| `POSTGRES_DB` | `control_tower_db` |

**Where to place:** `.env`  
**Used by:** `app/core/config.py` → `app/db/session.py` (SQLAlchemy engine) and `docker-compose.yml` (`db` service init, `api` service `DATABASE_URL` override).  
**Required for:** Every feature that stores or retrieves audit data (scans, reports, RAG chunks).  
**Fallback if missing:** Application fails to start — `sqlalchemy.exc.OperationalError` on startup.

> In Docker Compose, `DATABASE_URL` is **always overridden** by the compose file to use the internal `db` hostname (`@db:5432`), regardless of what `.env` contains. The `.env` value is only used when running the API directly on the host (outside Docker).

---

### OpenAI

| Variable | Placeholder Example |
|---|---|
| `OPENAI_API_KEY` | `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

**Where to place:** `.env` (uncomment the line)  
**Used by:** Not used by any current application code. The variable is a commented placeholder in `.env.example` for a future LLM integration.  
**Required for:** Nothing in the current codebase. All specialist agents in `app/agents/` run in **deterministic stub mode** today — pattern-based analysis without any LLM calls.  
**Fallback if missing:** No effect — the system already operates fully without this key.

---

### Anthropic Claude

| Variable | Placeholder Example |
|---|---|
| `ANTHROPIC_API_KEY` | `sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

**Where to place:** `.env` (uncomment the line)  
**Used by:** Not used by any current application code. Commented placeholder for a future LLM integration.  
**Required for:** Nothing in the current codebase (same as `OPENAI_API_KEY` above).  
**Fallback if missing:** No effect — the system already operates fully without this key.

---

### Grafana (Observability)

| Variable | Placeholder Example |
|---|---|
| `GRAFANA_ADMIN_PASSWORD` | `change-me-in-production` |

**Where to place:** `.env`  
**Used by:** Grafana container (mapped to `GF_SECURITY_ADMIN_PASSWORD` in `docker-compose.yml`).  
**Required for:** Accessing Grafana dashboards at `http://localhost:3012`.  
**Fallback if missing:** Defaults to `admin` — functional but insecure.

---

### RAG / Embedding (no external API key required)

The RAG pipeline (`app/rag/`) uses `sentence-transformers` with the `all-MiniLM-L6-v2` model, which runs **locally** — no API key is needed. If `sentence-transformers` is not installed, the system automatically falls back to `NullEmbeddingProvider` (zero vectors), and TF-IDF retrieval is used instead of vector search.

No environment variables control this behaviour; it is purely dependency-driven.

---

## 6. Docker Compose Environment Flow

```
.env file
   │
   ├─► docker-compose.yml: db service
   │       POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
   │       → initialises the PostgreSQL database on first run
   │
   ├─► docker-compose.yml: api service
   │       env_file: .env          ← all .env vars injected into container
   │       DATABASE_URL            ← overridden to use internal hostname 'db'
   │       ALLOWED_SCAN_PATHS      ← overridden with Docker-safe defaults
   │       HOST_REPOS_PATH         ← used in volume bind (not injected as var)
   │       │
   │       └─► app/core/config.py (Settings class)
   │               reads env vars via pydantic-settings
   │               provides typed settings to the application
   │
   ├─► docker-compose.yml: ui service
   │       API_BASE_URL: http://api:8000/api/v1
   │       │
   │       └─► ui/services/api_client.py (os.getenv)
   │               ui/main.py (os.getenv)
   │               ui/pages/page_settings.py (os.getenv)
   │
   └─► docker-compose.yml: grafana service
           GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD:-admin}
```

**Services:**

| Service | Container Name | Key Environment Variables |
|---|---|---|
| `db` | `control_tower_db` | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` |
| `api` | `control_tower_api` | All `.env` vars + `DATABASE_URL` (overridden), `ALLOWED_SCAN_PATHS` (overridden) |
| `ui` | `control_tower_ui` | `API_BASE_URL` (hardcoded to internal `api` hostname in compose) |
| `prometheus` | `control_tower_prometheus` | None (uses config file only) |
| `grafana` | `control_tower_grafana` | `GF_SECURITY_ADMIN_PASSWORD`, `GF_USERS_ALLOW_SIGN_UP` |

---

## 7. Local Development Setup

Run without Docker (requires a local PostgreSQL instance with pgvector):

```bash
# 1. Copy and configure environment
cp .env.example .env
# Edit .env: set DATABASE_URL to your local PostgreSQL

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Alembic migrations
alembic upgrade head

# 5. Start the API
uvicorn app.main:app --reload --port 8000

# 6. In a separate terminal, start the UI
streamlit run ui/main.py --server.port 8513
```

**Demo Mode (no backend, no database, no API keys):**

```bash
DEMO_MODE=true streamlit run ui/main.py
# or set DEMO_MODE=true in .env before running
```

---

## 8. Production / Deployment Notes

The repository ships Docker Compose only — no Kubernetes, Helm, or CI/CD files are present in the current codebase.

For production deployments:

1. **Secrets management:** Store `POSTGRES_PASSWORD`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `GRAFANA_ADMIN_PASSWORD` in your secrets manager (e.g., Docker Swarm secrets, AWS Secrets Manager, Azure Key Vault) rather than in `.env`.
2. **Override `.env` at runtime:** Pass variables through the shell environment, a secure env file, or a CI/CD secrets injection step before running `docker compose`.
3. **Do not use default database credentials** (`control_tower_pass`) in any environment reachable from the internet.
4. **Change `GRAFANA_ADMIN_PASSWORD`** from `admin` before exposing Grafana externally.
5. **`HOST_REPOS_PATH`** mounts as read-only (`:ro` flag in compose). Preserve this flag in any production deployment.

---

## 9. Safety Rules

- **Never commit `.env`** — add it to `.gitignore` (already present in this repo).
- **Commit only `.env.example`** — with placeholder values, never real secrets.
- **Use placeholder values only** in documentation and examples (e.g., `sk-proj-xxx`, `change-me`).
- **Rotate keys immediately** if a real key is accidentally committed to Git. Treat the key as compromised.
- **Scope provider keys** to minimum required permissions and set spending limits on LLM provider accounts.
- **Use Demo Mode** (`DEMO_MODE=true`) when demonstrating or presenting the system publicly — no backend, no keys, no data exposure.
- **The scanner mounts repositories read-only** (`:ro` Docker volume flag). Never remove this flag.
- **Secret masking** is applied by `app/scanner/secret_masker.py` to all scanned file content before it enters the RAG pipeline or reports — patterns include OpenAI keys, Anthropic keys, Google API keys, AWS access key IDs, GitHub tokens, and generic `PASSWORD=` / `SECRET=` / `API_KEY=` patterns.

---

## 10. Gaps and Recommended Improvements

| Gap | Status | Recommendation |
|---|---|---|
| `HOST_REPOS_PATH` not in `.env.example` | **Fixed** — added with placeholder `HOST_REPOS_PATH=/path/to/your/repos` and comment | No further action needed |
| `API_BASE_URL` not in `.env.example` | **Used but not documented in `.env.example`** | Add a commented entry so developers know it can be overridden for pointing the UI at a remote API |
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` load path | **Commented out in `.env.example`; loaded by OS env only — no Pydantic field** | Consider adding optional `openai_api_key` / `anthropic_api_key` fields to the `Settings` class (`app/core/config.py`) so validation and documentation are centralised |
| `CORS_ALLOWED_ORIGINS` in `.env.example` | **Commented out with no explanation of when to uncomment** | Add an inline comment explaining that this only needs changing for non-standard deployments |
| No secret validation on startup | **Absent** | Consider adding a startup check that warns (not fails) when `ALLOWED_SCAN_PATHS` is empty or `HOST_REPOS_PATH` is unset |
| `GF_SECURITY_ADMIN_PASSWORD` default is `admin` | **Insecure default** | Document prominently that this must be changed before any internet-facing deployment |

---

*Last updated: May 2026. Reflects repository state at Wave 6 completion.*
