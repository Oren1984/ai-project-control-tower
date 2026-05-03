# Workflow — AI Project Control Tower

## End-to-End Workflow

```
1. Setup → 2. Blueprint → 3. Scan → 4. Audit → 5. Review → 6. Export
```

### Step 1 — Setup

Navigate to the **Project Setup** page in the Streamlit UI (http://localhost:8513).

Create a new project:
- Project name (human-readable identifier)
- Description (optional)

The project record is stored in PostgreSQL and provides the context for all subsequent audits.

### Step 2 — Blueprint Upload

Navigate to the **Blueprint Upload** page.

Upload or paste a Blueprint document. The Blueprint is the desired state — an architecture specification, a requirements document, a technical design doc, or any text that describes what a good version of this project should look like.

The Blueprint is chunked, embedded (if an embedding provider is configured), and indexed for hybrid retrieval.

### Step 3 — Scan

Navigate to the **Audit Mode** page.

Set the repository path. The path must be inside `ALLOWED_SCAN_PATHS` (configured in `.env`).

The scanner:
- Resolves the path and validates it against the allowlist
- Reads all text files (skips binary, oversized, and `.git/` internals)
- Classifies files by type (Python, YAML, Markdown, etc.)
- Masks secrets in all content before indexing

### Step 4 — Audit Run

Select the project, blueprint, and audit mode:

| Mode | Description |
|---|---|
| `rag_only` | RAG retrieval and scoring without agent analysis |
| `agent_only` | Agent analysis without RAG retrieval context |
| `hybrid` | Full pipeline: RAG context feeds agent analysis |

Click **Run Audit**. The orchestrator dispatches 6 specialist agents in sequence:
- Architecture Agent
- RAG/AI Agent
- DevOps/MLOps Agent
- QA Agent
- Security Agent
- Documentation Agent

Each agent returns structured `FindingModel` objects with file evidence, severity, dimension, and recommendation text.

The scoring engine computes per-dimension and overall scores.

### Step 5 — Review

Navigate to:
- **Findings Dashboard** — filter findings by severity, dimension, or agent
- **Scores** page — view per-dimension scores
- **Audit History** — compare across multiple audit runs

Findings include:
- Severity: `critical` | `high` | `medium` | `low` | `info`
- Evidence: exact file path and content excerpt
- Dimension: one of the 9 audit dimensions
- Recommendation: descriptive text (never a patch or auto-fix)

### Step 6 — Export

Navigate to the **Final Report** page.

Download the report in your preferred format:

| Format | Use Case |
|---|---|
| Markdown | Human review, GitHub comments, Confluence |
| HTML | Presentation, browser viewing, sharing |
| JSON | Programmatic processing, dashboards, archiving |

---

## API-Driven Workflow

All steps above are available via the REST API:

```bash
# Create project
curl -X POST http://localhost:8013/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "my-project", "description": "Optional description"}'

# Upload blueprint
curl -X POST http://localhost:8013/api/v1/blueprints \
  -H "Content-Type: application/json" \
  -d '{"project_id": 1, "name": "v1", "content": "..."}'

# Run audit
curl -X POST http://localhost:8013/api/v1/audits/run \
  -H "Content-Type: application/json" \
  -d '{"project_id": 1, "blueprint_id": 1, "repo_path": "/path/to/repo", "mode": "hybrid"}'

# Download report
curl "http://localhost:8013/api/v1/audits/1/report?format=markdown"
```

Full API reference: [api.md](api.md)

---

## Audit Modes Comparison

| Mode | Speed | Coverage | Best For |
|---|---|---|---|
| `rag_only` | Fast | Blueprint alignment | Quick gap analysis |
| `agent_only` | Medium | Code structure | Structural review |
| `hybrid` | Slower | Maximum depth | Full audit |

---

## Data Flow Diagram

```
┌─────────────┐    POST /api/v1/audits/run
│  Streamlit  │ ─────────────────────────────────────────────────┐
│  UI (8513)  │                                                   ↓
└─────────────┘                                        ┌──────────────────┐
                                                       │  FastAPI (8013)  │
                                                       │                  │
                                                       │  1. Validate path │
                                                       │  2. Create run    │
                                                       └────────┬─────────┘
                                                                │
                                         ┌──────────────────────┼──────────────────────┐
                                         ↓                      ↓                      ↓
                                  ┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
                                  │   Scanner   │      │  RAG Layer   │      │    7 Agents     │
                                  │  (read-only)│      │  (hybrid)    │      │  (orchestrated) │
                                  └─────┬───────┘      └──────┬───────┘      └────────┬────────┘
                                        │                      │                       │
                                        └──────────────────────┴───────────────────────┘
                                                               ↓
                                                    ┌──────────────────────┐
                                                    │   Scoring Engine     │
                                                    │  (9 dimensions)      │
                                                    └──────────┬───────────┘
                                                               ↓
                                                    ┌──────────────────────┐
                                                    │  Report Generator    │
                                                    │  MD / HTML / JSON    │
                                                    └──────────────────────┘
```
