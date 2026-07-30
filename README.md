# AI Project Control Tower

## Oren Salami | AI Systems Engineer ## 

---

A local-first, read-only AI audit and governance system.

**This system never modifies an inspected repository. This is a hard invariant enforced by code, tests, and a mandatory E2E release gate.**

---

## Project Overview

AI Project Control Tower is a portfolio-grade AI systems engineering project demonstrating how to build a production-ready audit pipeline. It scans AI/MLOps/DevOps repositories, evaluates them against a defined Blueprint document, and produces structured audit reports with findings, evidence, severity scoring, and recommendations.

It is built for engineers who need a structured, explainable way to assess project quality without introducing automated changes.

---

## Purpose

- Give engineers a clear, scored view of how well a project meets a defined architecture blueprint
- Support structured human review without replacing human judgment
- Demonstrate a complete AI systems pipeline: scanning → RAG → multi-agent → structured report
- Provide an audit trail of findings with evidence, severity, and scoring

---

## Core Capabilities

| Capability | Description |
|---|---|
| Repository scanning | Read-only file traversal with path allowlist and secret masking |
| Blueprint comparison | Upload any markdown/text blueprint as the desired state |
| Hybrid RAG pipeline | TF-IDF + pgvector retrieval with Reciprocal Rank Fusion |
| 7 specialist agents | Architecture, RAG/AI, DevOps, QA, Security, Documentation, Orchestrator |
| 9-dimension scoring | Per-dimension and overall 0–100 scores |
| Structured reports | Markdown, HTML, and JSON export with sanitisation pass |
| Streamlit UI | 9-page interactive interface with Demo Mode |
| Observability | Prometheus metrics + pre-provisioned Grafana dashboard |
| Safety guardrails | 7 non-negotiable rules enforced in code and tests |
| Demo Mode | Full UI walkthrough without a running backend or API keys |

---

## Architecture & System Design

```
Streamlit UI (:8513)  ←HTTP→  FastAPI (:8013)  ←SQLAlchemy→  PostgreSQL+pgvector (:5433)
                                     ↑
                             Scanner + RAG + 7 Agents
                                     ↑
                     Prometheus (:9092) ← /metrics scrape
                             ↑
                     Grafana (:3012)
```

> **Docker networking note:** host ports are for browser access only. Inside Docker Compose,
> the UI container reaches the API at `http://api:8000` (internal port), not `:8013`.

Full architecture diagram: [docs/00-overview/architecture.md](docs/00-overview/architecture.md)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Database | PostgreSQL 16 + pgvector |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Settings | Pydantic Settings |
| Logging | structlog (JSON) |
| Metrics | prometheus-client |
| UI | Streamlit |
| Deployment | Docker Compose |

---

## Repository Structure

```
ai-project-control-tower/
├── app/                     # FastAPI backend (58 Python files)
│   ├── agents/              # 7 specialist audit agents
│   ├── api/routes/          # REST API endpoints
│   ├── audit/               # Audit engine + scoring
│   ├── core/                # Config, logging, metrics
│   ├── db/                  # SQLAlchemy models + session
│   ├── rag/                 # Hybrid RAG pipeline
│   ├── reports/             # Report generation + sanitisation
│   ├── scanner/             # File scanner + security layer
│   └── schemas/             # Pydantic schemas
├── ui/                      # Streamlit UI (9 pages + components + demo data)
├── tests/                   # Unit + integration + E2E tests
├── docs/                    # Architecture, API, deployment, testing, portfolio docs
├── static-demo/             # Portfolio static demo site (HTML/CSS/JS)
├── notebooks/               # Conceptual demo notebooks
├── observability/           # Prometheus config + Grafana dashboard
├── alembic/                 # Database migration scripts
├── Doces/                   # Source of truth planning documents
├── docker-compose.yml       # Full stack: API + DB + UI + Prometheus + Grafana
├── Dockerfile               # API service image
├── Dockerfile.ui            # Streamlit UI image
└── requirements.txt         # Python dependencies
```

---

## How to Run

### Option A — Demo Mode (no backend required)

Open the Streamlit UI with demo mode enabled — no Docker, no database, no API keys needed:

```bash
pip install streamlit
DEMO_MODE=true streamlit run ui/main.py --server.port 8513
```

Or toggle **🎭 Demo Mode** in the sidebar at any time after launch.

Demo mode pre-populates all 9 pages with realistic sample data:
- 1 project, 1 blueprint, 10 audit findings (high/medium/low/info)
- 9-dimension scores (overall 72/100)
- 3 audit history records
- Full markdown, HTML, and JSON reports

### Option B — Full Stack (Docker Compose)

#### 1. Copy environment file

```bash
cp .env.example .env
```

Edit `.env` and set `ALLOWED_SCAN_PATHS` to the directories you want to allow for scanning:

```bash
ALLOWED_SCAN_PATHS=["/home/user/projects"]
```

#### 2. Start the full stack

```bash
docker compose up --build
```

Starts: PostgreSQL · FastAPI · Streamlit · Prometheus · Grafana

> **Stale volume note:** If you see `FATAL: database "control_tower" does not exist` in
> logs, a Docker volume from a previous run may have a different database name. Reset it:
> ```bash
> docker compose down -v
> docker compose up --build
> ```

#### 3. Run database migrations (first time only)

```bash
docker compose exec api alembic upgrade head
```

#### 4. Open the UI

http://localhost:8513

---

## Docker

All services are defined in `docker-compose.yml`:

| Service | Host Port | Container Port | Purpose |
|---|---|---|---|
| db | 5433 | 5432 | PostgreSQL 16 + pgvector |
| api | 8013 | 8000 | FastAPI backend |
| ui | 8513 | 8501 | Streamlit frontend |
| prometheus | 9092 | 9090 | Metrics collection |
| grafana | 3012 | 3000 | Dashboards (admin / admin) |

### Service URLs (host access)

| URL | Service |
|---|---|
| http://localhost:8513 | Streamlit UI |
| http://localhost:8013/docs | FastAPI OpenAPI docs |
| http://localhost:8013/api/v1/health | API health check |
| http://localhost:9092 | Prometheus |
| http://localhost:3012 | Grafana (admin / admin) |

---

## Evaluation Workflow

1. **Create a project** — name and describe the repository you want to audit
2. **Upload a Blueprint** — paste or upload your architecture specification
3. **Run a scan** — the scanner reads the target repository (read-only)
4. **Run an audit** — agents evaluate the repository against the blueprint
5. **Review findings** — view scores, findings, and evidence in the UI
6. **Download the report** — export as Markdown, HTML, or JSON

Full workflow guide: [docs/03-audit-workflow/workflow.md](docs/03-audit-workflow/workflow.md)

---

## Reports / Outputs

```bash
# Markdown
curl "http://localhost:8013/api/v1/audits/1/report?format=markdown"

# JSON
curl "http://localhost:8013/api/v1/audits/1/report?format=json"

# HTML
curl "http://localhost:8013/api/v1/audits/1/report?format=html"
```

Each report includes overall score, per-dimension scores, findings with evidence and severity, and audit metadata.

---

## Demo Notebooks

Conceptual demo notebooks are available in `notebooks/`.

The notebook (`notebooks/01_project_control_tower_demo.ipynb`) uses static sample data to illustrate the data model, finding structure, scoring, and report generation. It requires no running backend and no API keys.

```bash
pip install jupyter
jupyter notebook notebooks/
```

See [notebooks/README.md](notebooks/README.md) for details.

---

## Static Portfolio Site

A portfolio-ready static site is available at `static-demo/index.html`.

To open locally:

```bash
cd static-demo
python -m http.server 8012
```

Then open http://localhost:8012

The site covers: workflow, audit dimensions, architecture, safety boundaries, demo report cards (labeled as static examples), and portfolio narrative.

---

## Testing

```bash
# Unit + integration tests
pytest

# With coverage
pytest --cov=app --cov-report=term-missing

# Integration (requires live database)
docker compose up -d db
pytest tests/integration/ -v

# E2E safety gate
pytest tests/e2e/test_no_repo_modification.py -v
```

Full test matrix: [docs/04-quality-security/testing.md](docs/04-quality-security/testing.md)

---

## E2E Validation

The mandatory E2E test (`tests/e2e/test_no_repo_modification.py`) verifies the core safety invariant: **no file in a target repository is created, modified, or deleted during any audit run.** This test is a hard release gate.

Validation commands:

```bash
curl http://localhost:8013/api/v1/health
curl http://localhost:8013/api/v1/ready
curl http://localhost:8013/metrics | head -20

docker compose exec db psql -U control_tower -d control_tower_db \
  -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

See [docs/03-audit-workflow/e2e-validation-summary.md](docs/03-audit-workflow/e2e-validation-summary.md) for the full checklist.

---

## Observability

```bash
# Prometheus metrics endpoint
curl http://localhost:8013/metrics | head -20

# Grafana dashboard
open http://localhost:3012  # admin / admin
```

11 Prometheus metrics pre-defined. Grafana dashboard (`observability/grafana/dashboards/control_tower.json`) is pre-provisioned — no manual setup needed.

See [docs/04-quality-security/observability.md](docs/04-quality-security/observability.md) for details.

---

## Security

| Rule | Enforcement |
|---|---|
| Never modify a target repository | E2E test is a release gate |
| Never execute target code | Scanner reads text only |
| Never auto-fix findings | Report sanitiser removes patch content |
| Never log provider API keys | structlog configuration |
| Only scan allowed paths | PathValidator on every audit request |
| Skip binary and oversized files | FileClassifier + size check |
| Mask secrets in all output | SecretMasker + ReportSanitiser |

See [docs/04-quality-security/security.md](docs/04-quality-security/security.md) for details.

---

## What This Project Demonstrates

- **RAG pipeline design** — hybrid TF-IDF + pgvector with RRF fusion, built from scratch
- **Multi-agent orchestration** — 7 specialist agents with Pydantic-typed structured output
- **Safety-first architecture** — non-modification invariant enforced at multiple layers
- **Observability** — structured JSON logs + Prometheus metrics + Grafana dashboard
- **DevOps** — Docker Compose full stack, Alembic migrations, comprehensive pytest suite
- **Portfolio presentation** — Demo Mode, static site, notebooks, and full documentation

Full portfolio narrative: [docs/00-overview/portfolio-summary.md](docs/00-overview/portfolio-summary.md)

---

## Current Status

| Wave | Scope | Status |
|---|---|---|
| 1 | FastAPI + PostgreSQL + pgvector + Alembic + structlog | Complete |
| 2 | Scanner + path allowlist + secret masking + security guardrails | Complete |
| 3 | RAG layer (hybrid TF-IDF + pgvector) + 7 audit agents + audit engine | Complete |
| 4 | Report generation (MD/HTML/JSON) + Streamlit UI (9 pages) | Complete |
| 5 | Full test matrix + Prometheus + Grafana + security tests + docs | Complete |
| 6 | Portfolio docs + static demo site + notebooks + Demo Mode | Complete |

---

## Known Limitations

- No API authentication (local-only design)
- No rate limiting on audit endpoints
- Real LLM output requires provider API keys in `.env`; default agents use deterministic stubs
- Audits are synchronous (one at a time)
- Jupyter notebooks parsed as raw JSON only
- pgvector semantic search requires a configured embedding provider

Full list: [docs/04-quality-security/known_limitations.md](docs/04-quality-security/known_limitations.md)

---

## Documentation

| File | Purpose |
|---|---|
| [docs/01-usage/USER_GUIDE.md](docs/01-usage/USER_GUIDE.md) | Step-by-step UI usage guide |
| [docs/02-installation/INSTALLATION.md](docs/02-installation/INSTALLATION.md) | Installation and setup guide |
| [docs/02-installation/deployment.md](docs/02-installation/deployment.md) | Deployment guide |
| [docs/00-overview/architecture.md](docs/00-overview/architecture.md) | System architecture and data flow |
| [docs/00-overview/project-overview.md](docs/00-overview/project-overview.md) | Detailed project overview |
| [docs/00-overview/portfolio-summary.md](docs/00-overview/portfolio-summary.md) | Portfolio narrative |
| [docs/01-usage/demo-instructions.md](docs/01-usage/demo-instructions.md) | Demo and interview instructions |
| [docs/03-audit-workflow/api.md](docs/03-audit-workflow/api.md) | API reference |
| [docs/03-audit-workflow/workflow.md](docs/03-audit-workflow/workflow.md) | End-to-end workflow guide |
| [docs/03-audit-workflow/e2e-validation-summary.md](docs/03-audit-workflow/e2e-validation-summary.md) | E2E validation checklist |
| [docs/04-quality-security/testing.md](docs/04-quality-security/testing.md) | Test matrix and instructions |
| [docs/04-quality-security/observability.md](docs/04-quality-security/observability.md) | Metrics, logging, Grafana |
| [docs/04-quality-security/security.md](docs/04-quality-security/security.md) | Security guardrails |
| [docs/04-quality-security/known_limitations.md](docs/04-quality-security/known_limitations.md) | Current limitations |
| [docs/04-quality-security/qa-summary.md](docs/04-quality-security/qa-summary.md) | QA and validation summary |
| [docs/05-cleanup/CLEANUP_REVIEW.md](docs/05-cleanup/CLEANUP_REVIEW.md) | Repository cleanup review |
| [CLAUDE.md](CLAUDE.md) | Engineering contract |
| [Doces/](Doces/) | Source of truth planning documents |

---

## Final Note

AI Project Control Tower is intentionally lean. It does exactly what it says: it reads, analyses, scores, and reports. It does not write, patch, or decide. The safety invariant — never modifying an inspected repository — is not a limitation. It is the core design principle.

---

## License

MIT

---
