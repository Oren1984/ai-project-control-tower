# Decos — AI Project Control Tower Planning Documents

This folder contains the full planning package for the `AI Project Control Tower` project.

## Files

```text
00_FULL_WORK_PLAN.md
01_CLAUDE_IMPLEMENTATION_PROMPT.md
02_BUILD_RULES.md
03_TESTING_OBSERVABILITY_SECURITY.md
04_AUDIT_REPORT_TEMPLATE.md
```

## Purpose

These documents define:

- What the system is
- Why it exists
- How it should be built
- What must be added
- What must not be added
- Safety boundaries
- Database direction
- RAG / Agent / Hybrid strategy
- Testing requirements
- Observability requirements
- Security requirements
- Final audit report structure

## Important Principle

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

## How To Use With Claude

Paste the content of:

```text
01_CLAUDE_IMPLEMENTATION_PROMPT.md
```

Then tell Claude:

```text
Read the Decos folder, scan the full repository, and produce the implementation planning report.
Do not write code yet.
Do not modify files.
Do not delete files.
Do not execute code.
```
