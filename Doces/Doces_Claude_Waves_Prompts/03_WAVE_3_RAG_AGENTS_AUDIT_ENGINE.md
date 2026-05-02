# Common Execution Rules — AI Project Control Tower

Repository:

```text
ai-project-control-tower
```

Important:
The documentation folder is named `Doces`.
Use `Doces` consistently everywhere.
Do not create a `Decos` folder.

Before starting:
1. Read the entire `Doces` folder.
2. Read the previous planning report if it exists.
3. Scan the current repository structure.
4. Work only on the requested wave.
5. Keep the implementation lean, working, and aligned with `Doces`.

Non-negotiable rules:

```text
Recommendation Only.
No Auto Fix.
No Generate Fix Plan.
No repository modification logic for inspected target repositories.
No automatic refactor of inspected target repositories.
No patching system.
No target repository code execution.
No React.
No SQLite.
PostgreSQL + pgvector from day one.
Streamlit UI only.
```

Do not modify:
- `Doces` content, unless explicitly requested.
- `AI-System-Templates-Library` content.
- `Project-Blueprint-System` content.

Do not create empty placeholder files.
Only create files required for the current wave.

At the end, always provide a completion report with:

```text
# Wave Completion Report

## Files Created
## Files Updated
## Files Not Touched
## What Was Implemented
## How To Run
## How To Test
## Validation Commands
## Known Limitations
## Next Recommended Wave
```


# Wave 3 Prompt — RAG + Agents + Audit Engine

Execute **Wave 3 only**.

Wave 1 and Wave 2 must already exist and pass validation.

## Wave 3 Scope

Build the core intelligence layer:

```text
RAG layer
Agent audit layer
Audit engine
Scoring engine
Finding schema
Audit context
Hybrid execution flow
```

## Important Implementation Rule

Start with local and deterministic behavior first.

Build in this order:

```text
1. RAG structure with TF-IDF support
2. pgvector retrieval support
3. Hybrid retrieval
4. Heuristic/local agent behavior
5. LLM provider abstraction
6. Optional provider wiring only if clean and safe
```

The system must work without API keys.

## RAG Layer

Required files:

```text
app/rag/
app/rag/chunker.py
app/rag/indexer.py
app/rag/tfidf_retriever.py
app/rag/vector_retriever.py
app/rag/hybrid_retriever.py
app/rag/embedding_provider.py
app/rag/rag_service.py
app/schemas/rag_schemas.py
```

Required retrieval modes:

```text
TF-IDF
pgvector
hybrid
```

Required behavior:

```text
Chunk documents
Support overlap
Preserve metadata
Store source path
Store content hash
Retrieve top-k context
Fallback safely if embeddings are unavailable
```

## Agent Layer

Required agents:

```text
app/agents/base_agent.py
app/agents/orchestrator_agent.py
app/agents/architecture_agent.py
app/agents/rag_ai_agent.py
app/agents/devops_mlops_agent.py
app/agents/qa_agent.py
app/agents/security_agent.py
app/agents/documentation_agent.py
app/schemas/agent_schemas.py
```

Do not add more agents in this wave.

All agents must return the same typed finding schema.

Every finding must include:

```text
category
severity
title
description
evidence
recommendation
file_path when available
line_number when available
```

Forbidden fields:

```text
auto_fix
fix_plan
patch
diff
generated_code
```

## Agent Modes

Support:

```text
RAG Only
Agent Only
Hybrid
```

For V1, if full LLM reasoning is not ready, use deterministic/heuristic logic and prepare interfaces for future provider wiring.

## Audit Engine

Required files:

```text
app/audit/
app/audit/audit_engine.py
app/audit/scoring.py
app/audit/models.py
```

Audit engine flow:

```text
Create audit_run
Run scanner
Index documents into RAG
Run orchestrator according to mode
Collect findings
Persist findings
Persist agent reviews if implemented
Compute scores
Update audit_run status
Return audit result
```

## Scoring

Implement 9 score dimensions:

```text
overall
architecture
qa
security
devops
mlops
documentation
rag_agent
observability
```

Use severity weighting:

```text
critical
high
medium
low
info
```

Keep scoring simple and explainable.

## Tests

Add tests for:

```text
Chunking
Overlap
TF-IDF retrieval
pgvector retrieval if practical
Hybrid retrieval
Agent output schema
No forbidden auto-fix fields
Audit engine happy path
Scoring logic
No target repository modification after audit
```

## End Requirement

Do not build Streamlit UI yet.
Do not build report generator beyond minimal internal structures unless required.
Do not build Prometheus/Grafana yet.
Stop after Wave 3 and provide the completion report.
