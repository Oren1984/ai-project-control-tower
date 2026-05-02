# AI Project Control Tower — Build Rules

## 1. Core Rule

This system is an external audit and recommendation system.

It must never modify the target repository.

```text
Read files.
Analyze content.
Generate report.
Do not execute target code.
Do not modify target files.
```

---

## 2. Forbidden Features

Do not build:

- Auto-fix
- Generate Fix Plan
- Automatic patching
- Automatic refactor
- Repository write mode
- Code rewrite mode
- Hidden file deletion
- Shell execution on target repo
- React UI
- SQLite-first DB
- Hard dependency on one LLM provider
- Enterprise SaaS complexity

---

## 3. Required Features

Build:

- FastAPI backend
- Streamlit UI
- PostgreSQL + pgvector
- Repository scanner
- Blueprint reader
- Flexible RAG
- Agent audit team
- Hybrid audit mode
- Findings model
- Scoring model
- Report generator
- Full tests
- Security guardrails
- Observability
- Docker Compose

---

## 4. Required Agents

Use only these initial agents:

1. Orchestrator Agent
2. Architecture Agent
3. RAG / AI Agent Reviewer
4. DevOps / MLOps Agent
5. QA Agent
6. Security Agent
7. Documentation Agent

Do not add more agents in V1 unless there is a strong reason.

---

## 5. Required Audit Outputs

Every finding should include:

```text
category
severity
title
description
evidence
recommendation
file_path
line_number, if available
```

Recommendations must be high-level and manual.

They must not become automatic fix instructions.

---

## 6. Required Export Formats

Support:

```text
Markdown
JSON
HTML
```

Markdown is the primary report format.

---

## 7. Required UI Tabs

Streamlit tabs:

```text
Project Setup
Blueprint Upload / Select
Audit Mode
Repository Scan
Findings Dashboard
Scores
Final Report
Audit History
Settings / Providers
```

---

## 8. Required Provider Settings

The system should allow configuration for:

```text
Local
OpenAI
Claude
Gemini
```

Providers must be optional and configurable.

The system must not be locked to one provider.

---

## 9. Required Retrieval Modes

The system should support:

```text
TF-IDF
pgvector
hybrid
```

The design must allow future extension.

---

## 10. Required Safety Controls

Implement:

```text
Path validation
Path allowlist
Max file size limit
Binary file skipping
Secret masking
Provider key masking
Report sanitization
No target code execution
No target repo modification
```
