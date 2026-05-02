# Portfolio Summary — AI Project Control Tower

## One-Line Summary

A local-first, read-only AI audit system that evaluates software projects against a Blueprint using a hybrid RAG pipeline and 7 specialist agents, producing structured reports without ever modifying the inspected repository.

---

## Problem

AI engineering projects often drift from their initial design. By the time a team notices, the codebase has diverged from the architecture blueprint in ways that are hard to quantify. Standard code review catches individual changes but misses systemic gaps: missing test coverage, undocumented components, security patterns that were never implemented.

There is no standard tool that:
1. Accepts a Blueprint (desired state) as input
2. Compares an actual codebase against it systematically
3. Produces scored, evidence-based findings across multiple quality dimensions
4. Does all of this without touching the target project

---

## Solution

AI Project Control Tower is a structured audit pipeline built on modern AI systems primitives:

- **Scanner** — safe, allowlisted, read-only file traversal with secret masking
- **RAG pipeline** — hybrid TF-IDF + pgvector retrieval, Blueprint-indexed, used as agent context
- **7 specialist agents** — each responsible for one quality domain
- **Scoring engine** — 9 dimensions, 0–100 scale, with per-finding severity
- **Report generator** — Markdown, HTML, JSON with sanitisation pass
- **Streamlit UI** — 9-page interactive interface for setup, audit, and report review

The safety model is non-negotiable: the system cannot modify the target repository at any layer. This is enforced architecturally and verified by a mandatory E2E release gate.

---

## Engineering Value

This project demonstrates end-to-end AI systems engineering:

| Skill | Demonstrated By |
|---|---|
| RAG pipeline design | Hybrid TF-IDF + pgvector with RRF fusion, chunking, embedding abstraction |
| Multi-agent orchestration | 7 typed agents with Pydantic output schemas, orchestrator coordination |
| FastAPI service design | Async endpoints, dependency injection, OpenAPI auto-docs, metrics endpoint |
| PostgreSQL + pgvector | Production-grade vector store, pgvector extension, SQLAlchemy ORM |
| Alembic migrations | Versioned schema evolution with upgrade/downgrade scripts |
| Structured logging | structlog JSON logs with request IDs and context propagation |
| Prometheus metrics | 11 metric types covering audit duration, agent calls, RAG queries |
| Docker Compose stack | 5-service compose with health checks, volume persistence, service dependencies |
| Pydantic schemas | Typed API contracts, settings management, typed finding models |
| pytest suite | Unit + integration + E2E, asyncio support, coverage reporting |

---

## AI Systems Value

From an AI engineering perspective, this project covers:

- **Retrieval-Augmented Generation (RAG)** — designed from scratch, not library-wrapped
- **Hybrid retrieval** — TF-IDF (lexical) + pgvector (semantic) fused with Reciprocal Rank Fusion
- **Agent design** — each agent has a clear scope, typed output, and evidence requirement
- **Structured output** — `FindingModel` with severity, dimension, evidence, recommendation
- **Context management** — RAG retrieval feeds agent context; pipeline is composable and swappable
- **Provider abstraction** — embedding provider is configurable; agents can use any LLM backend

---

## DevOps / MLOps Value

- Docker Compose full stack — reproducible from cold start in one command
- Alembic database migrations — schema evolution without data loss
- Prometheus + Grafana — production observability from day one
- E2E release gate — safety invariant tested on every run
- Structured JSON logs — machine-parseable, ELK/Splunk compatible
- Health + readiness endpoints — Kubernetes-ready probe pattern

---

## Safety Model

The safety model is a first-class design concern:

1. **PathValidator** — every audit request validates the repo path against `ALLOWED_SCAN_PATHS`
2. **FileClassifier** — binary files and files > 1 MB are skipped before reading
3. **SecretMasker** — credential patterns are masked before any content is stored or returned
4. **ReportSanitiser** — report content is scanned for auto-fix language and removed
5. **No execution** — the scanner opens files in text mode only; no subprocess calls on target code
6. **No auto-fix** — agents return findings, not patches; the report format has no patch section
7. **E2E release gate** — `test_no_repo_modification.py` verifies the invariant on every release

This model is appropriate for use in enterprises or regulated environments where tools that access production codebases must be provably read-only.

---

## What It Demonstrates

For a technical interviewer or hiring manager, this project shows:

1. **I can design and build a complete AI pipeline** — not just the ML model but the surrounding system
2. **I understand production concerns** — observability, migrations, containerisation, safety
3. **I can reason about safety in AI systems** — the non-modification invariant is real and enforced
4. **I structure AI output** — typed schemas, severity classification, evidence citations
5. **I build for auditability** — every finding has a trace back to a file and a reason
6. **I document as I build** — architecture docs, API docs, test docs, deployment guides

---

## How I Would Present It in an Interview

**Opening (30 seconds):**

> "This is an AI audit system — you point it at a codebase, give it an architecture blueprint, and it tells you how well the project matches the blueprint. It uses a hybrid RAG pipeline to index the blueprint, dispatches 7 specialist agents against the repository, and produces a scored report with evidence-backed findings across 9 quality dimensions."

**Key technical point (1 minute):**

> "The interesting engineering challenge was designing the safety model. The system analyses code but must never touch it. I enforced this at multiple layers: a path allowlist, a secret masker, a report sanitiser that strips auto-fix content, and a mandatory E2E test that verifies no target file changes after an audit run. That test is a hard release gate — you cannot ship without it passing."

**AI systems depth (1 minute):**

> "The RAG pipeline is hybrid: TF-IDF for lexical retrieval and pgvector for semantic similarity, fused with Reciprocal Rank Fusion. The embedding provider is abstracted so it can be swapped. Each agent receives top-K chunks as context, returns Pydantic-typed `FindingModel` objects, and the orchestrator aggregates them into a scored report."

**DevOps / production angle (30 seconds):**

> "The whole thing runs on Docker Compose in one command: five services — API, database with pgvector, Streamlit UI, Prometheus, and Grafana. Alembic migrations, structlog JSON logs, health and readiness endpoints. The observability story is complete from day one — that's a deliberate design choice, not an afterthought."
