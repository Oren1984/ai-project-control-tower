# Claude Implementation Prompt — AI Project Control Tower

You are working inside the repository:

```text
ai-project-control-tower
```

The folder `Decos` contains the full product and engineering plan for the system.

Your task in this stage is **not to write code yet**.

## Your Current Task

1. Read the entire `Decos` folder.
2. Scan the full repository structure.
3. Compare the current repository state against the documentation in `Decos`.
4. Produce a clear implementation plan.
5. Explain what should be added, updated, deleted, or kept.
6. Give improvement and efficiency recommendations.
7. Do not write code.
8. Do not modify files.
9. Do not generate patches.
10. Do not execute the target system.

## Required Output

Create a detailed planning response with the following structure:

```text
# AI Project Control Tower — Implementation Planning Report

## 1. Repository Scan Summary
- Existing folders
- Existing files
- Important assets
- Missing expected components

## 2. Understanding of the Project
- What the system is
- Why it exists
- What it must do
- What it must never do

## 3. Alignment With Decos
- What already matches the plan
- What is missing
- What needs to be updated
- What should not be changed

## 4. Recommended Implementation Phases
Phase 1 — Foundation
Phase 2 — Database + Models
Phase 3 — Repository Scanner
Phase 4 — RAG Layer
Phase 5 — Agent Audit Layer
Phase 6 — Audit Engine + Scoring
Phase 7 — Report Generator
Phase 8 — Streamlit UI
Phase 9 — Testing
Phase 10 — Observability + Security
Phase 11 — Documentation Finalization

## 5. What Should Stay
List all folders/files that should remain and why.

## 6. What Should Be Added
List new folders/files/modules that should be added and why.

## 7. What Should Be Updated
List existing folders/files that should be updated and why.

## 8. What Should Be Deleted
List anything that should be deleted.
If nothing should be deleted, say clearly:
"Nothing should be deleted at this stage."

## 9. Risk Review
- Technical risks
- Security risks
- Scope risks
- Testing risks
- Over-engineering risks

## 10. Recommendations
Give practical recommendations for building the system cleanly, safely, and modularly.

## 11. No-Code Confirmation
Confirm that you did not write code, modify files, delete files, or execute project code.
```

## Non-Negotiable Project Rules

The system is an audit and recommendation tool only.

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

You must preserve this principle in the implementation plan.

## Required Technical Direction

The system must be designed around:

```text
FastAPI backend
Streamlit UI only
PostgreSQL + pgvector
SQLAlchemy
Alembic
Flexible RAG
Agent audit layer
Hybrid mode
Markdown / JSON / HTML reports
Prometheus + Grafana
Full testing matrix
Security guardrails
Docker Compose
```

Do not recommend React for this project.

Do not recommend SQLite for this project.

Do not recommend auto-fix features.

## Expected Mindset

Review the project from the perspective of:

```text
MLOps Engineer
Applied AI Engineer
DevOps Engineer
QA Engineer
Security-aware system reviewer
Architecture reviewer
```

Focus on:

- What
- Why
- How
- Safety
- Modularity
- Testing
- Observability
- Maintainability
- Portfolio-grade clarity
