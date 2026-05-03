# Demo Instructions — AI Project Control Tower

## Static Demo Site

### Open locally

```bash
python -m http.server 8099 -d static-demo
```

Then open: http://localhost:8099

No dependencies required — pure HTML, CSS, and JavaScript.

### What to show

1. **Hero section** — explain what the project does in one sentence
2. **What It Does / What It Doesn't Do** — the recommendation-only model is a key differentiator
3. **Workflow cards** — walk through the 6-step audit workflow
4. **Audit Dimensions** — show the 9 quality dimensions with descriptions
5. **Demo Report Card** — walk through a static example finding (labeled clearly as a demo)
6. **Safety Boundaries** — emphasise the non-modification invariant
7. **Portfolio section** — close with the engineering narrative

---

## Running the Full Application

### Prerequisites

- Docker and Docker Compose installed
- At least 4 GB RAM available for the full stack

### Start the stack

```bash
# Copy env file
cp .env.example .env

# Edit .env and set the scan path allowlist
# ALLOWED_SCAN_PATHS=["/path/to/your/repos"]

# Build and start everything
docker compose up --build

# Run migrations (first time only)
docker compose exec api alembic upgrade head
```

### Open the UI

http://localhost:8513 — Streamlit interface

### Open the API docs

http://localhost:8013/docs — FastAPI interactive OpenAPI documentation

---

## Interview Demo Script

### 60-Second Summary

> "AI Project Control Tower is a read-only audit system for software projects. You give it a target repository and an architecture blueprint. It runs a hybrid RAG pipeline to index the blueprint, dispatches 7 specialist agents against the repository, and produces a scored audit report across 9 quality dimensions. The core invariant: it never modifies the inspected repository. That is enforced in code, tested with a mandatory E2E release gate, and hardwired into the report sanitiser."

### What to Show First

1. **Static demo site** — opens without Docker, gives the full concept overview
2. **Streamlit UI** at http://localhost:8513 (if Docker is running)
3. **Walk the workflow**: Project → Blueprint → Scan → Audit → Review → Report
4. **Findings dashboard** — show severity filtering and dimension breakdown
5. **E2E test**: `pytest tests/e2e/test_no_repo_modification.py -v`
6. **API docs** at http://localhost:8013/docs

### Talking Points

| Topic | What to Say |
|---|---|
| Why read-only? | "Tools that touch production codebases carry real risk. I designed this to be provably read-only — the constraint is not a missing feature, it is a deliberate safety choice enforced at every layer." |
| Why RAG? | "The Blueprint is the source of truth. RAG lets agents query the blueprint semantically at analysis time rather than loading it all into a prompt window." |
| Why 7 agents? | "Each agent has a well-defined scope and evidence requirement. Decomposing by domain keeps each agent focused and its output auditable." |
| Why Prometheus? | "Observability is not optional in production AI systems. Every audit can be traced through structured JSON logs, Prometheus metrics, and per-request request IDs — not just inspected after a failure." |
| Why Streamlit not React? | "Streamlit keeps the UI in Python, matching the rest of the stack. It avoids a separate frontend build toolchain and is production-capable for this use case." |
| Why pgvector not a cloud vector DB? | "Local-first design. No external service dependency, no data leaving the machine, no API cost. pgvector is production-grade and runs in the same Docker Compose stack." |

---

## Running Tests for a Demo

```bash
# E2E non-modification test (the key demo test)
pytest tests/e2e/test_no_repo_modification.py -v

# Full test suite
pytest --tb=short

# With coverage report
pytest --cov=app --cov-report=term-missing
```

---

## Validation Commands

```bash
# Health
curl http://localhost:8013/api/v1/health

# Readiness (confirms DB connection)
curl http://localhost:8013/api/v1/ready

# Prometheus metrics
curl http://localhost:8013/metrics | head -30

# pgvector extension active
docker compose exec db psql -U control_tower -d control_tower_db \
  -c "SELECT * FROM pg_extension WHERE extname = 'vector';"

# Schema tables
docker compose exec db psql -U control_tower -d control_tower_db -c "\dt"
```

---

## Known Issues During Demo

| Issue | Resolution |
|---|---|
| LLM agents return stubs | Configure `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in `.env` for live AI output |
| Semantic search falls back to TF-IDF | Configure `EMBEDDING_PROVIDER` in `.env`; TF-IDF still produces valid results |
| First `docker compose up --build` is slow | Run it before the demo (3–5 minutes on first build) |
| Streamlit session resets on refresh | Navigate to Audit History to retrieve completed audits from the database |
| Port conflicts | Check ports 8013, 8513, 5433, 9092, 3012 are free before starting |
