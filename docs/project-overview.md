# Project Overview — AI Project Control Tower

## What Is It?

AI Project Control Tower is a local-first, read-only AI audit system. It accepts a target repository path and a Blueprint document, runs a multi-agent analysis pipeline, and produces a structured audit report.

It is not an autonomous code reviewer. It does not fix code. It does not generate patch files. It provides structured observations with evidence, severity classifications, and recommendations for human engineers to act on.

## Origin

The project addresses a real problem in AI/MLOps engineering: there is no standard way to compare what was planned (the Blueprint) against what was actually built. Code reviews cover individual changes; audits cover the whole system.

Control Tower provides a repeatable, structured audit process driven by AI agents and documented in machine-readable formats.

## Scope

**In scope:**
- Static analysis of repository file structure and content
- Comparison against a user-supplied Blueprint document
- Multi-agent evaluation across 7 quality domains
- Scoring and finding generation (read-only)
- Structured report export (Markdown, HTML, JSON)

**Out of scope:**
- Autonomous code modification
- Git history analysis
- Runtime testing or code execution
- Authentication or multi-user access control
- Production deployment without additional hardening

## System Context

```
Engineer → uploads Blueprint → creates Project → triggers Audit Run
                                                       ↓
                                             FastAPI processes request
                                                       ↓
                                        Scanner reads target repo (read-only)
                                                       ↓
                                     RAG pipeline indexes Blueprint chunks
                                                       ↓
                                   7 agents evaluate against Blueprint context
                                                       ↓
                                  Scoring engine computes 9-dimension scores
                                                       ↓
                                 Report generator produces MD / HTML / JSON
                                                       ↓
                             Engineer reviews findings and acts (or does not act)
```

## Quality Dimensions

Audits evaluate repositories across 9 dimensions:

| # | Dimension | What It Measures |
|---|---|---|
| 1 | Architecture | Layer separation, patterns, module boundaries |
| 2 | RAG / AI | RAG design quality, retrieval strategy, AI components |
| 3 | DevOps / MLOps | CI/CD, pipelines, deployment configs |
| 4 | Testing / QA | Test coverage, quality gates, E2E tests |
| 5 | Security | Credential exposure, unsafe patterns, access controls |
| 6 | Documentation | README completeness, docstrings, ADRs, diagrams |
| 7 | Observability | Logging, metrics, tracing, dashboards |
| 8 | Data Management | Schema, migrations, storage patterns |
| 9 | Overall | Weighted aggregate of all dimensions |

## Design Philosophy

- **Human in the loop** — the system recommends, humans decide
- **Read-only by design** — modification of inspected repositories is architecturally impossible
- **Evidence-based findings** — every finding cites the file path and content that triggered it
- **Structured output** — findings are typed, scored, and machine-readable
- **Local-first** — no cloud dependencies, runs entirely on Docker Compose
- **Transparency** — structlog JSON logs and Prometheus metrics expose all system behaviour
