# AI Project Control Tower — Full Work Plan

## 1. Project Identity

**Project Name:** AI Project Control Tower  
**Root Documentation Folder:** `Decos`  
**Primary Purpose:**  
A local-first AI project audit and governance system that scans existing AI / MLOps / DevOps repositories, compares them against a Blueprint document, evaluates the real implementation, and produces structured audit reports with findings, evidence, severity, scoring, and recommendation-only guidance.

This system is designed first for personal use by Oren as an MLOps / Applied AI Engineer / DevOps / QA practitioner, and second as a portfolio-grade project that demonstrates architecture, governance, testing, observability, and AI system evaluation.

---

## 2. Core Project Definition

The system is **not** a code generator and **not** an auto-fix tool.

It is an external audit layer that works above existing projects.

It should:

- Scan a target repository end-to-end.
- Read the project Blueprint / specification document.
- Read README files, docs, configuration, source code, tests, CI/CD files, Docker files, and hidden files.
- Build a complete repository inventory.
- Compare planned architecture against actual implementation.
- Evaluate architecture, RAG, agents, DevOps, MLOps, QA, security, observability, UI/UX, and documentation.
- Produce a professional audit report.
- Provide recommendations explaining **what**, **why**, and **how** at a high level.
- Never modify the target repository.

---

## 3. Non-Negotiable Safety Rules

These are fixed project rules.

```text
Recommendation Only.
No Auto Fix.
No Generate Fix Plan.
No repository modification.
No automatic refactor.
No automatic patching.
No writing into the target repository.
No execution of target project code by default.
```

The system may explain:

- What the issue is.
- Why it matters.
- How to think about solving it.
- What kind of tool or process may help.

The system must not:

- Rewrite code.
- Patch files.
- Delete files.
- Rename folders.
- Generate detailed patch instructions that can be blindly executed.
- Run untrusted code from the inspected repository.

This keeps the tool safe, professional, and suitable for QA / Governance use.

---

## 4. Why This Project Exists

This project was created from lessons learned while building multiple AI engineering systems.

It connects and audits the user’s ecosystem:

- `Project-Blueprint-System`
- `AI-System-Templates-Library`
- RAG systems
- Agent systems
- DevOps / Docker / CI/CD
- QA / E2E / Testing
- Security / Monitoring
- UI / UX / Docs
- FastAPI / Streamlit / React-based systems
- DS / ML / DL / NLP / LLM / Agent projects

The project shows that the engineer does not only build systems, but also knows how to:

- Review systems.
- Measure quality.
- Compare implementation to planning.
- Detect gaps.
- Manage technical risk.
- Produce structured engineering reports.
- Improve engineering workflows.

---

## 5. Target Users

### Primary User

Oren — as a personal AI Engineering Control Tower for reviewing his own projects.

### Secondary Use Case

Portfolio demonstration for technical reviewers, managers, instructors, or interviewers.

The project should look professional, but it is not intended to become a heavy enterprise SaaS platform.

---

## 6. Core Architecture

Final technical stack:

```text
Backend: FastAPI
UI: Streamlit only
Database: PostgreSQL + pgvector from day one
ORM: SQLAlchemy
Migrations: Alembic
RAG: Flexible retrieval layer
Agents: Modular audit agents
Reports: Markdown / JSON / HTML
Observability: Prometheus + Grafana
Security: Read-only scanning, masking, validation
Deployment: Docker Compose
```

React is intentionally excluded from this project.

The UI is a working internal audit dashboard, not a marketing product.

---

## 7. Operating Modes

The system must support three modes:

| Mode | Purpose |
|---|---|
| RAG Only | Reads Blueprint, README, docs, standards, templates, and prior knowledge |
| Agent Only | Performs reasoning, categorization, scoring, and audit review |
| Hybrid | Combines retrieval + agents for deep audit review |

The main mode is **Hybrid**.

---

## 8. RAG Strategy

The RAG layer must be flexible and not locked to one provider or one method.

Required retrieval options:

- Local TF-IDF
- PostgreSQL + pgvector
- Hybrid Search
- Optional external LLM providers
- Optional Claude / Gemini / GPT integration
- No hard dependency on one paid API provider

The retrieval layer must support:

- Blueprint indexing
- README indexing
- Docs indexing
- Source-code-aware text indexing
- Audit history indexing
- Report indexing
- Chunking
- Overlap
- Metadata tracking
- File path tracking
- Source hashing

---

## 9. Agent Team

Do not build dozens of agents in V1.  
Use a small, strong, clear team.

### 9.1 Orchestrator Agent

Responsibilities:

- Receive project name, repo path, and Blueprint.
- Start repository scan.
- Trigger RAG retrieval.
- Assign work to audit agents.
- Collect findings.
- Normalize outputs.
- Generate unified audit summary.
- Send final structure to the report generator.

### 9.2 Architecture Agent

Checks:

- Folder structure
- Separation of concerns
- OOP / modularity
- Coupling
- Config management
- API structure
- Backend organization
- Scalability readiness
- Maintainability

### 9.3 RAG / AI Agent Reviewer

Checks:

- Whether RAG exists
- Chunking strategy
- Overlap strategy
- Retrieval flexibility
- Provider abstraction
- Whether the system is locked to one provider
- Fallback / demo mode
- Separation between LLM provider and business logic
- Agent orchestration logic
- Prompt organization
- Tool usage boundaries

### 9.4 DevOps / MLOps Agent

Checks:

- Docker
- Docker Compose
- `.env.example`
- Healthchecks
- CI/CD
- Deployment readiness
- Logging
- Observability
- Kubernetes readiness if relevant
- Model / data / pipeline readiness if relevant

### 9.5 QA Agent

Checks:

- Unit tests
- Integration tests
- E2E tests
- Test coverage structure
- Test naming
- README accuracy
- Validation docs
- Known limitations
- QA audit documents
- Whether docs match the real implementation

### 9.6 Security Agent

Checks:

- Secrets
- `.env`
- Hardcoded keys
- Dependency risk indicators
- Basic auth checks
- Rate limiting
- Input validation
- Access control
- Path traversal risks
- Report sanitization
- Secret masking

### 9.7 Documentation Agent

Checks:

- README
- Architecture docs
- API docs
- Run instructions
- Project status
- Deployment docs
- Testing docs
- Mismatch between docs and code
- Missing “known limitations”
- Missing “current status”

---

## 10. Database Decision

The project starts directly with:

```text
PostgreSQL + pgvector
```

No SQLite-first approach.

Reason:

- The system needs audit history.
- The system needs project comparisons.
- The system needs semantic search.
- The system needs document chunks and embeddings.
- The system needs report indexing.
- Avoid future DB refactor.

---

## 11. Recommended Database Schema

### projects

```text
id
name
repo_path
repo_url
description
created_at
updated_at
```

### blueprints

```text
id
project_id
name
file_path
content_hash
created_at
```

### audit_runs

```text
id
project_id
blueprint_id
mode
status
started_at
completed_at
overall_score
architecture_score
qa_score
security_score
devops_score
mlops_score
documentation_score
rag_agent_score
```

### findings

```text
id
audit_run_id
category
severity
title
description
evidence
recommendation
file_path
line_number
status
created_at
```

### reports

```text
id
audit_run_id
report_type
file_path
created_at
```

### knowledge_sources

```text
id
project_id
source_type
source_path
content_hash
indexed_at
```

### documents

```text
id
project_id
source_id
file_path
content
content_hash
metadata
created_at
```

### document_chunks

```text
id
document_id
chunk_index
content
metadata
embedding
created_at
```

### agent_reviews

```text
id
audit_run_id
agent_name
status
summary
raw_output
created_at
```

---

## 12. UI Decision — Streamlit Only

The UI is built with Streamlit.

Recommended tabs:

```text
1. Project Setup
2. Blueprint Upload / Select
3. Audit Mode
4. Repository Scan
5. Findings Dashboard
6. Scores
7. Final Report
8. Audit History
9. Settings / Providers
```

Settings should include:

- LLM Provider: Local / OpenAI / Claude / Gemini
- Retrieval Mode: TF-IDF / pgvector / hybrid
- Audit Mode: RAG / Agent / Hybrid
- Severity Threshold
- Export Format: Markdown / JSON / HTML

---

## 13. Repository Scanner Requirements

The scanner must:

- Scan the entire repository recursively.
- Include visible and hidden files.
- Build a full file inventory.
- Identify file types.
- Skip binary files safely.
- Apply maximum file size limits.
- Mask secrets.
- Calculate content hash.
- Track file path and metadata.
- Avoid executing code.
- Avoid modifying files.

The scanner should identify:

- README files
- Docs
- Source code
- Tests
- Docker files
- Compose files
- CI/CD workflows
- `.env.example`
- `.gitignore`
- Hidden config files
- Package files
- Requirements files
- Lock files
- Kubernetes manifests
- Terraform files if present

---

## 14. Audit Categories

The audit should cover:

```text
Architecture
RAG / AI System Design
Agent System Design
DevOps
MLOps
QA
Testing
Security
Observability
Documentation
UI / UX
Database Design
API Design
Deployment Readiness
Maintainability
```

---

## 15. Final Report Structure

The final report should be generated in Markdown first, with optional JSON and HTML exports.

Recommended structure:

```text
# AI Project Audit Report

## 1. Executive Summary
## 2. Project Overview
## 3. Blueprint Alignment
## 4. Repository Structure Review
## 5. Architecture Review
## 6. RAG / Agent Review
## 7. DevOps / MLOps Review
## 8. QA & Testing Review
## 9. Security Review
## 10. Observability Review
## 11. Documentation Review
## 12. Critical Findings
## 13. Medium Findings
## 14. Low Priority Findings
## 15. Recommendations
## 16. Suggested Manual Next Steps
## 17. Final Score
## 18. Known Limitations of This Audit
```

Important:  
Recommendations must be high-level and manual.  
The report must not include an auto-fix plan.

---

## 16. Scoring Model

Recommended scoring categories:

```text
overall_score
architecture_score
qa_score
security_score
devops_score
mlops_score
documentation_score
rag_agent_score
observability_score
```

Example:

```text
overall_score: 82/100
architecture_score: 85/100
qa_score: 70/100
security_score: 78/100
devops_score: 88/100
mlops_score: 80/100
documentation_score: 90/100
rag_agent_score: 84/100
observability_score: 76/100
```

Severity levels:

```text
Critical
High
Medium
Low
Info
```

---

## 17. Testing Strategy

The project must include a full testing system.

Required test types:

```text
Unit Tests
Integration Tests
API Tests
DB Tests
RAG Retrieval Tests
Agent Output Tests
Security Tests
Report Generation Tests
E2E Tests
```

### 17.1 Scanner Tests

Verify:

- Normal folder scanning
- Hidden file scanning
- Safe binary skipping
- File inventory generation
- Hash generation
- File size policy
- No crash on unusual files

### 17.2 RAG Tests

Verify:

- Chunking
- Overlap
- Indexing
- pgvector search
- TF-IDF search
- Hybrid retrieval
- Metadata preservation
- Fallback if embeddings are unavailable

### 17.3 Agent Tests

Verify:

- Each agent returns valid schema
- Category is valid
- Severity is valid
- Recommendation exists
- No auto-fix output
- No file modifications
- Orchestrator merges outputs correctly

### 17.4 DB Tests

Verify:

- Project creation
- Blueprint creation
- Audit run creation
- Findings persistence
- Reports persistence
- Chunks persistence
- Relationships
- Migrations

### 17.5 API Tests

Required endpoints to test:

```text
GET  /api/v1/health
GET  /api/v1/ready
POST /api/v1/projects
POST /api/v1/audits/run
GET  /api/v1/audits/{id}
GET  /api/v1/audits/{id}/findings
GET  /api/v1/audits/{id}/report
```

### 17.6 Security Tests

Verify:

- API keys are not printed
- Secrets are masked
- `.env` content is not exposed in reports
- Hardcoded secrets are detected
- Path traversal is blocked
- Input validation works
- CORS is controlled
- Basic rate limiting exists

### 17.7 E2E Tests

Main E2E scenario:

```text
1. Create project
2. Upload/select Blueprint
3. Scan repository
4. Run Hybrid audit
5. Save findings
6. Generate report
7. Validate report content
8. Confirm no files were modified
```

The last point is mandatory.

---

## 18. Observability Requirements

The system must include:

```text
Structured Logging
Request IDs
Audit Run IDs
Prometheus Metrics
Grafana Dashboard
Health Endpoint
Ready Endpoint
Error Logs
```

Recommended metrics:

```text
audit_runs_total
audit_runs_failed_total
audit_duration_seconds
files_scanned_total
findings_total
findings_by_severity
rag_queries_total
rag_retrieval_latency_seconds
agent_reviews_total
agent_review_duration_seconds
report_generation_total
api_request_duration_seconds
db_query_errors_total
```

### Health Endpoint

```text
GET /api/v1/health
```

Checks whether the app is alive.

### Ready Endpoint

```text
GET /api/v1/ready
```

Checks:

- DB connection
- pgvector availability
- Writable storage path
- Provider configuration
- RAG index availability if relevant

---

## 19. Security Requirements

Because this system reads repositories, security must be high.

Required rules:

```text
Read-only audit mode
No file modification
No command execution on target repo
No shell execution by default
Path allowlist
Secret masking
Safe file readers
Binary file skipping
Max file size limit
Provider key masking
Report sanitization
```

The system must read and analyze files only.

It must not execute target project code.

---

## 20. Recommended Initial Repository Structure

```text
ai-project-control-tower/
│
├── Decos/
│   ├── 00_FULL_WORK_PLAN.md
│   ├── 01_CLAUDE_IMPLEMENTATION_PROMPT.md
│   ├── 02_BUILD_RULES.md
│   ├── 03_TESTING_OBSERVABILITY_SECURITY.md
│   └── 04_AUDIT_REPORT_TEMPLATE.md
│
├── app/
│   ├── api/
│   ├── core/
│   ├── scanners/
│   ├── rag/
│   ├── agents/
│   ├── audit/
│   ├── reports/
│   ├── db/
│   └── main.py
│
├── ui/
│   └── streamlit_app.py
│
├── data/
│   ├── projects/
│   ├── blueprints/
│   ├── reports/
│   └── knowledge_base/
│
├── docs/
│   ├── architecture.md
│   ├── audit_methodology.md
│   ├── agent_roles.md
│   ├── rag_strategy.md
│   ├── scoring_model.md
│   └── known_limitations.md
│
├── tests/
│
├── docker-compose.yml
├── Dockerfile
├── README.md
└── .env.example
```

---

## 21. Build Scope

The implementation should focus on:

```text
FastAPI backend
PostgreSQL + pgvector
Streamlit UI
Repository scanner
Blueprint loader
RAG indexing/retrieval
Agent audit layer
Hybrid audit execution
Findings model
Scoring model
Report generator
Testing system
Security guardrails
Observability
Docker Compose
```

---

## 22. What Should Be Added

Add:

- `Decos` documentation folder
- Project brief
- Build rules
- Claude prompt
- FastAPI app structure
- Streamlit UI
- PostgreSQL + pgvector setup
- SQLAlchemy models
- Alembic migrations
- Scanner module
- RAG module
- Agent module
- Audit engine
- Report generator
- Tests
- Prometheus metrics
- Grafana dashboard
- Security validation

---

## 23. What Should Stay

Keep:

- `Project-Blueprint-System`
- `AI-System-Templates-Library`
- Existing reusable templates
- Existing Blueprint documents
- Existing Shared Library content
- Existing prompt strategy where relevant

These are foundation assets.

---

## 24. What Should Not Be Added

Do not add:

- React UI
- Auto-fix engine
- Generate Fix Plan feature
- Code patching system
- Repository write mode
- Enterprise multi-user SaaS complexity
- Heavy Kubernetes setup in V1
- Hard dependency on one LLM provider
- Hard dependency on paid APIs
- Automatic execution of target repository code

---

## 25. Final Build Philosophy

The system must be:

```text
Local-first
Safe
Read-only
Modular
Provider-flexible
RAG/Agent/Hybrid
Report-oriented
Tested
Observable
Secure
Useful for personal workflow
Strong enough for portfolio
Not over-engineered
```

Final sentence:

**AI Project Control Tower is the management and audit layer above Oren’s AI engineering ecosystem.**
