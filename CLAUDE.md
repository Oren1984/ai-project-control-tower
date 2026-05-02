# CLAUDE.md — Engineering Contract

## Source of Truth

`Doces` is the source of truth for this project.
Read `Doces` before making any implementation decision.

## Non-Negotiable Rules

- **Recommendation Only** — this system recommends, never auto-fixes.
- **No Auto Fix** — do not generate or apply fixes to inspected repositories.
- **No Generate Fix Plan** — do not produce step-by-step patch instructions.
- **No inspected repo modification** — never write, delete, or rename files in a target repository.
- **No target code execution** — never run code from an inspected repository.
- **No React** — Streamlit UI only.
- **No SQLite** — PostgreSQL + pgvector only.
- **PostgreSQL + pgvector only** — from day one, no migration from SQLite later.
- **Streamlit UI only** — no React, no Next.js, no other frontend framework.

## Wave Discipline

- Work only on the requested wave.
- Do not build Wave N+1 components during Wave N.
- Do not modify `Doces`, `AI-System-Templates-Library`, or `Project-Blueprint-System`.
- Do not create empty placeholder files.
- End every wave with a Wave Completion Report.

## Architecture Anchors

- Backend: FastAPI
- UI: Streamlit
- Database: PostgreSQL + pgvector
- ORM: SQLAlchemy
- Migrations: Alembic
- Settings: Pydantic Settings
- Logging: structlog (structured JSON)
- Metrics: prometheus-client
- Deployment: Docker Compose

## Wave Status

| Wave | Scope | Status |
|---|---|---|
| 1 | FastAPI + DB + Alembic + structlog | Complete |
| 2 | Scanner + path allowlist + secret masking | Complete |
| 3 | RAG + 7 agents + audit engine | Complete |
| 4 | Reports + Streamlit UI | Complete |
| 5 | Tests + Prometheus + Grafana + docs | Complete |
| 6 | Notebooks + static site + Copilot handoff | Complete |
