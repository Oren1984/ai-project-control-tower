# Architecture — AI Project Control Tower

## Overview

The Control Tower is a local-first, read-only AI audit system. It scans a target repository, compares it against a Blueprint document, and produces structured audit reports with findings, evidence, and severity scores. It never modifies the target repository.

## Component Map

```
┌─────────────────────────────────────────────────────────┐
│              Streamlit UI  host:8513 / internal:8501     │
│  Project Setup │ Blueprint Upload │ Audit │ Reports ...  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP (internal: http://api:8000)
┌────────────────────────▼────────────────────────────────┐
│          FastAPI Backend  host:8013 / internal:8000      │
│                                                         │
│  /api/v1/health    /api/v1/ready    /metrics            │
│  /api/v1/projects  /api/v1/audits   /api/v1/reports     │
│                                                         │
│  ┌──────────────┐  ┌───────────┐  ┌──────────────────┐ │
│  │  Audit Engine│  │ RAG Layer │  │  Report Generator│ │
│  │  (7 agents)  │  │ (hybrid)  │  │  (md/html/json)  │ │
│  └──────┬───────┘  └─────┬─────┘  └──────────────────┘ │
│         │                │                               │
│  ┌──────▼────────────────▼─────────────────────────┐    │
│  │             Scanner + Security Layer             │    │
│  │  PathValidator │ SecretMasker │ FileClassifier   │    │
│  └─────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────┘
                         │ SQLAlchemy
┌────────────────────────▼────────────────────────────────┐
│      PostgreSQL 16 + pgvector  host:5433 / internal:5432 │
│  projects │ blueprints │ audit_runs │ findings           │
│  rag_documents │ rag_document_chunks │ reports           │
└─────────────────────────────────────────────────────────┘

┌──────────────────────────┐    ┌─────────────────────┐
│ Prometheus  host:9092    │◄───│ /metrics scrape      │
└──────────┬───────────────┘    └─────────────────────┘
           │
┌──────────▼───────────────┐
│ Grafana  host:3012        │
│ control_tower.json        │
└───────────────────────────┘
```

> Host ports are for browser/curl access. Container-to-container traffic uses internal ports.

## Data Flow — Audit Run

```
1. User selects project + blueprint + repo path in UI
2. UI POSTs /api/v1/audits/run
3. API creates AuditRun record (status=running)
4. Scanner reads files (read-only, sha256-verified)
5. RAG indexer chunks documents and builds hybrid index
   (TF-IDF + pgvector embeddings)
6. Orchestrator dispatches 6 specialist agents:
   Architecture · RAG/AI · DevOps/MLOps · QA · Security · Documentation
7. Each agent returns a list of FindingModel objects
8. Scoring engine computes 9-dimension scores + overall
9. AuditRun updated (status=completed, overall_score)
10. Report generator produces markdown / HTML / JSON
11. Report sanitizer removes secrets and auto-fix content
12. Report stored in DB, available for download
```

## Agents

| Agent | Responsibility |
|---|---|
| Orchestrator | Coordinates all agents, aggregates results |
| Architecture | Validates project structure, layers, patterns |
| RAG/AI | Reviews AI/ML quality, RAG design, vector stores |
| DevOps/MLOps | Checks CI/CD, pipelines, deployment configs |
| QA | Reviews test coverage, quality gates |
| Security | Detects credential leaks, unsafe patterns |
| Documentation | Assesses README completeness, docstrings, ADRs |

## RAG Layer

Hybrid retrieval: TF-IDF (BM25-like lexical) + pgvector (semantic).

```
Blueprint text
     ↓
  Chunker (paragraph / sliding-window)
     ↓
  TF-IDF index (scikit-learn)     pgvector embeddings (if provider configured)
     ↓                                     ↓
        Hybrid Retriever (RRF fusion)
                    ↓
              Top-K chunks → agent context
```

## Security Invariants

- Target repositories are **never modified**. The E2E test is a release gate.
- Path allowlist (`ALLOWED_SCAN_PATHS`) restricts which directories can be scanned.
- Path traversal (`../`) is resolved and checked against the allowlist.
- Binary files and files > 1 MB are skipped.
- Secrets are masked in all log output and reports.
- Provider API keys are never logged.

## Technology Stack

| Layer | Choice | Reason |
|---|---|---|
| Backend | FastAPI | Async, typed, OpenAPI auto-docs |
| Database | PostgreSQL 16 + pgvector | Production-grade, native vector search |
| ORM | SQLAlchemy 2.x | Mature, typed queries |
| Migrations | Alembic | Safe, versioned schema evolution |
| UI | Streamlit | Python-native, no React |
| Logging | structlog (JSON) | Structured, machine-readable |
| Metrics | prometheus-client | Standard Prometheus exposition |
| Deployment | Docker Compose | Local-first, reproducible |
