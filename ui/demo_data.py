"""Static sample data for the Streamlit UI demo/mock mode.

Used by api_client.py when DEMO_MODE is active.
All data is fabricated for portfolio presentation purposes.
"""
from __future__ import annotations

DEMO_PROJECTS = [
    {
        "id": 1,
        "name": "sample-mlops-pipeline",
        "repo_path": "/home/demo/repos/sample-mlops-pipeline",
        "description": "Sample MLOps training and serving pipeline — demo project",
        "created_at": "2026-05-01T10:00:00Z",
    }
]

DEMO_BLUEPRINTS = [
    {
        "id": 1,
        "project_id": 1,
        "name": "MLOps Platform Architecture v1",
        "file_path": "/home/demo/repos/sample-mlops-pipeline/BLUEPRINT.md",
        "created_at": "2026-05-01T10:05:00Z",
    }
]

DEMO_SCORES = {
    "overall": 72,
    "architecture": 78,
    "qa": 65,
    "security": 58,
    "devops": 71,
    "mlops": 74,
    "documentation": 85,
    "rag_agent": 69,
    "observability": 76,
}

DEMO_FINDINGS = [
    {
        "id": 1,
        "audit_run_id": 1,
        "agent_name": "security",
        "category": "security",
        "severity": "high",
        "title": "No authentication layer on API endpoints",
        "description": (
            "The FastAPI application exposes audit and project endpoints without "
            "authentication middleware. Any process with network access can trigger audits."
        ),
        "evidence": "app/api/routes/audits.py: @router.post('/run') has no auth dependency injected",
        "recommendation": (
            "Add OAuth2 bearer token or API key authentication middleware for production deployments. "
            "Document the network isolation requirement for local-only use."
        ),
        "file_path": "app/api/routes/audits.py",
        "line_number": 24,
    },
    {
        "id": 2,
        "audit_run_id": 1,
        "agent_name": "security",
        "category": "security",
        "severity": "medium",
        "title": "CORS configuration defaults to permissive localhost origins",
        "description": (
            "Default CORS policy allows multiple localhost ports. "
            "Appropriate for local development but should be restricted for any network-accessible deployment."
        ),
        "evidence": "app/core/config.py: cors_allowed_origins includes localhost:8513 and localhost:3012",
        "recommendation": "Restrict allowed origins to exactly the UI origin in non-development environments.",
        "file_path": "app/core/config.py",
        "line_number": None,
    },
    {
        "id": 3,
        "audit_run_id": 1,
        "agent_name": "devops_mlops",
        "category": "devops",
        "severity": "medium",
        "title": "Synchronous audit execution blocks the API process",
        "description": (
            "Audit runs are synchronous operations that block the uvicorn worker for their full duration. "
            "Concurrent audit requests will serialize."
        ),
        "evidence": "app/audit/audit_engine.py: run_audit() is a blocking synchronous call",
        "recommendation": (
            "Move long-running audits to a background task queue "
            "(Celery, ARQ, or FastAPI BackgroundTasks) for production workloads."
        ),
        "file_path": "app/audit/audit_engine.py",
        "line_number": None,
    },
    {
        "id": 4,
        "audit_run_id": 1,
        "agent_name": "qa",
        "category": "qa",
        "severity": "medium",
        "title": "Integration tests auto-skip without live database",
        "description": (
            "4 integration tests are marked to auto-skip when PostgreSQL is unreachable. "
            "CI pipelines may report all-pass without validating database interactions."
        ),
        "evidence": "tests/integration/: 4 tests with conditional skip when DB unreachable",
        "recommendation": "Provision a test PostgreSQL instance in CI (GitHub Actions service containers).",
        "file_path": "tests/integration/",
        "line_number": None,
    },
    {
        "id": 5,
        "audit_run_id": 1,
        "agent_name": "architecture",
        "category": "architecture",
        "severity": "low",
        "title": "RAG hybrid retrieval correctly implements RRF fusion",
        "description": (
            "HybridRetriever correctly combines TF-IDF lexical and pgvector semantic results "
            "using Reciprocal Rank Fusion. Implementation matches Blueprint specification."
        ),
        "evidence": "app/rag/hybrid_retriever.py: _rrf_fusion() correctly merges both retrieval sources",
        "recommendation": "Well implemented. Consider making the k parameter in RRF configurable via settings.",
        "file_path": "app/rag/hybrid_retriever.py",
        "line_number": None,
    },
    {
        "id": 6,
        "audit_run_id": 1,
        "agent_name": "documentation",
        "category": "documentation",
        "severity": "low",
        "title": "API reference documentation is complete and accurate",
        "description": "All API endpoints are documented with request/response schemas and example payloads.",
        "evidence": "docs/api.md: 186 lines covering all /api/v1 routes",
        "recommendation": "Documentation meets Blueprint requirements. Consider adding OpenAPI Redoc export.",
        "file_path": "docs/api.md",
        "line_number": None,
    },
    {
        "id": 7,
        "audit_run_id": 1,
        "agent_name": "rag_ai",
        "category": "rag_agent",
        "severity": "low",
        "title": "Embedding provider abstraction supports multiple backends",
        "description": (
            "EmbeddingProvider class is correctly abstracted to support multiple providers "
            "and falls back to TF-IDF cleanly when none is configured."
        ),
        "evidence": "app/rag/embedding_provider.py: configurable backend with clean fallback",
        "recommendation": "Consider adding a local embedding model (sentence-transformers) to remove API key dependency.",
        "file_path": "app/rag/embedding_provider.py",
        "line_number": None,
    },
    {
        "id": 8,
        "audit_run_id": 1,
        "agent_name": "devops_mlops",
        "category": "observability",
        "severity": "info",
        "title": "Prometheus metrics and Grafana dashboard are pre-provisioned",
        "description": "11 Prometheus metrics defined; 9-panel Grafana dashboard pre-provisioned in the repository.",
        "evidence": "app/core/metrics.py (11 metrics), observability/grafana/dashboards/control_tower.json (9 panels)",
        "recommendation": "Observability layer matches Blueprint requirements. No changes needed.",
        "file_path": "app/core/metrics.py",
        "line_number": None,
    },
    {
        "id": 9,
        "audit_run_id": 1,
        "agent_name": "qa",
        "category": "qa",
        "severity": "info",
        "title": "E2E non-modification release gate is present and passing",
        "description": (
            "Mandatory E2E release gate verifies: no file in a target repository is created, "
            "modified, or deleted during any audit run."
        ),
        "evidence": "tests/e2e/test_no_repo_modification.py: 5 tests, all passing, SHA-256 hash verified",
        "recommendation": "Safety invariant correctly enforced. Ensure this runs in all CI pipelines.",
        "file_path": "tests/e2e/test_no_repo_modification.py",
        "line_number": None,
    },
    {
        "id": 10,
        "audit_run_id": 1,
        "agent_name": "architecture",
        "category": "architecture",
        "severity": "info",
        "title": "Alembic migrations follow correct versioning pattern",
        "description": "3 migration files present with correct down_revision chains. Strategy matches Blueprint.",
        "evidence": "alembic/versions/: 0001_init, 0002_wave3_rag_agents_findings, 0003_wave4_reports",
        "recommendation": "Migration strategy is correct. No changes needed.",
        "file_path": "alembic/versions/",
        "line_number": None,
    },
]

DEMO_AUDIT_RESULT = {
    "audit_run_id": 1,
    "project_id": 1,
    "project_name": "sample-mlops-pipeline",
    "blueprint_id": 1,
    "mode": "hybrid",
    "status": "completed",
    "total_findings": len(DEMO_FINDINGS),
    "scores": DEMO_SCORES,
    "started_at": "2026-05-02T10:10:00Z",
    "completed_at": "2026-05-02T10:12:45Z",
}

DEMO_AUDIT_HISTORY = [
    {
        "id": 1,
        "project_id": 1,
        "blueprint_id": 1,
        "mode": "hybrid",
        "status": "completed",
        "overall_score": 72,
        "created_at": "2026-05-02T10:10:00Z",
        "started_at": "2026-05-02T10:10:00Z",
        "completed_at": "2026-05-02T10:12:45Z",
    },
    {
        "id": 2,
        "project_id": 1,
        "blueprint_id": 1,
        "mode": "agent_only",
        "status": "completed",
        "overall_score": 68,
        "created_at": "2026-05-01T14:30:00Z",
        "started_at": "2026-05-01T14:30:00Z",
        "completed_at": "2026-05-01T14:32:10Z",
    },
    {
        "id": 3,
        "project_id": 1,
        "blueprint_id": 1,
        "mode": "rag_only",
        "status": "completed",
        "overall_score": 71,
        "created_at": "2026-04-30T09:15:00Z",
        "started_at": "2026-04-30T09:15:00Z",
        "completed_at": "2026-04-30T09:16:55Z",
    },
]

DEMO_REPORT_MARKDOWN = """\
# AI Project Audit Report — sample-mlops-pipeline

> ⚠️ **This is a demo report generated from static sample data.**

**Project:** sample-mlops-pipeline
**Blueprint:** MLOps Platform Architecture v1
**Mode:** hybrid
**Status:** completed
**Overall Score:** 72 / 100
**Date:** 2026-05-02

---

## Executive Summary

The audit evaluated `sample-mlops-pipeline` against the MLOps Platform Architecture Blueprint v1.
The project scores **72/100** overall, with notable strengths in Documentation (85) and Architecture (78).
Primary areas for improvement are Security (58) and QA (65).

No critical findings were identified. The E2E non-modification release gate passes — the target repository
is never modified during audits.

---

## Dimension Scores

| Dimension | Score |
|---|---|
| Architecture | 78 / 100 |
| QA / Testing | 65 / 100 |
| Security | 58 / 100 |
| DevOps | 71 / 100 |
| MLOps | 74 / 100 |
| Documentation | 85 / 100 |
| RAG / Agents | 69 / 100 |
| Observability | 76 / 100 |
| **Overall** | **72 / 100** |

---

## Findings

### [HIGH] No authentication layer on API endpoints

- **Agent:** security · **File:** `app/api/routes/audits.py` line 24

**Evidence:**
```
@router.post('/run') has no auth dependency injected
```

**Recommendation:** Add OAuth2 bearer token or API key authentication for production deployments.

---

### [MEDIUM] Synchronous audit execution blocks the API process

- **Agent:** devops_mlops · **File:** `app/audit/audit_engine.py`

**Evidence:**
```
run_audit() is a blocking synchronous call — no background task queue
```

**Recommendation:** Move long-running audits to a background task queue for production workloads.

---

### [MEDIUM] CORS defaults to permissive localhost origins

- **Agent:** security · **File:** `app/core/config.py`

**Recommendation:** Restrict allowed CORS origins in non-development environments.

---

### [MEDIUM] Integration tests auto-skip without live database

- **Agent:** qa · **File:** `tests/integration/`

**Recommendation:** Provision a test PostgreSQL instance in CI pipelines.

---

### [LOW] RAG hybrid retrieval correctly implements RRF fusion ✓

- **Agent:** architecture · **File:** `app/rag/hybrid_retriever.py`

Implementation matches Blueprint specification.

---

### [INFO] E2E non-modification release gate passing ✓

- **Agent:** qa · **File:** `tests/e2e/test_no_repo_modification.py`

5/5 tests passing. Core safety invariant verified.

---

### [INFO] Prometheus metrics and Grafana dashboard pre-provisioned ✓

- **Agent:** devops_mlops

Observability matches Blueprint requirements. No changes needed.

---

*Generated by AI Project Control Tower. Recommendations are for human review only.*
*No code modifications have been made or suggested as patches.*
"""

DEMO_REPORT_JSON = """\
{
  "project_name": "sample-mlops-pipeline",
  "blueprint_name": "MLOps Platform Architecture v1",
  "mode": "hybrid",
  "status": "completed",
  "note": "DEMO — static sample data",
  "overall_score": 72,
  "scores": {
    "architecture": 78, "qa": 65, "security": 58,
    "devops": 71, "mlops": 74, "documentation": 85,
    "rag_agent": 69, "observability": 76, "overall": 72
  },
  "total_findings": 10,
  "findings": [
    {"severity": "high",   "agent": "security",     "title": "No authentication layer on API endpoints"},
    {"severity": "medium", "agent": "security",     "title": "CORS configuration defaults to permissive origins"},
    {"severity": "medium", "agent": "devops_mlops", "title": "Synchronous audit execution blocks API process"},
    {"severity": "medium", "agent": "qa",           "title": "Integration tests auto-skip without live database"},
    {"severity": "low",    "agent": "architecture", "title": "RAG hybrid retrieval correctly implements RRF fusion"},
    {"severity": "low",    "agent": "documentation","title": "API reference documentation complete and accurate"},
    {"severity": "low",    "agent": "rag_ai",       "title": "Embedding provider abstraction supports multiple backends"},
    {"severity": "info",   "agent": "devops_mlops", "title": "Prometheus metrics and Grafana dashboard pre-provisioned"},
    {"severity": "info",   "agent": "qa",           "title": "E2E non-modification release gate is present and passing"},
    {"severity": "info",   "agent": "architecture", "title": "Alembic migrations follow correct versioning pattern"}
  ],
  "audit_date": "2026-05-02T10:12:45Z"
}
"""
