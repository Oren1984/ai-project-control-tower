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


# Wave 5 Prompt — Full Testing + Observability + Final Docs

Execute **Wave 5 only**.

Wave 1 through Wave 4 must already exist and pass validation.

## Wave 5 Scope

Finalize the engineering quality layer:

```text
Full test matrix
Observability
Prometheus
Grafana
Structured logs
Security hardening
Documentation finalization
README final update
Deployment docs
Known limitations
Architecture docs
```

## Testing Requirements

Implement or complete the full test matrix:

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

## Mandatory E2E Test

The most important E2E test must prove:

```text
The inspected target repository was not modified.
```

Flow:

```text
Copy sample target repo to temp directory
Record sha256 of every file before audit
Run full hybrid audit
Generate report
Record sha256 of every file after audit
Assert hashes are identical
Assert no files added
Assert no files deleted
Assert file count unchanged
```

This test is a release gate.

## Observability

Add:

```text
Structured JSON logging
Request IDs
Audit Run IDs
Prometheus metrics
Grafana dashboard
/metrics endpoint
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

Required folders:

```text
observability/
observability/prometheus/prometheus.yml
observability/grafana/datasources/
observability/grafana/dashboards/control_tower.json
```

## Security Hardening

Ensure:

```text
CORS is controlled
Rate limiting exists where practical
Path allowlist works
Path traversal is blocked
Secrets are masked
Reports are sanitized
Provider keys are never logged
No target code execution exists
No target repo modification exists
Binary files are skipped
Oversized files are skipped
```

## Docker Compose

Update Docker Compose for final local stack:

```text
api
ui
db
prometheus
grafana
```

Keep it simple and local-first.

## Documentation Finalization

Create/update:

```text
README.md
CLAUDE.md
docs/architecture.md
docs/api.md
docs/deployment.md
docs/testing.md
docs/observability.md
docs/security.md
docs/known_limitations.md
```

README must include:

```text
Project purpose
Architecture
Tech stack
How to run
How to test
How to run audit
How to download reports
Safety rules
Known limitations
Current status
```

## Final Validation

Run and report:

```text
docker compose build
docker compose up
health endpoint check
ready endpoint check
pytest
E2E non-modification test
basic UI access
report generation validation
```

If you cannot run a command, explain exactly why and provide the command for the user to run.

## End Requirement

Do not create notebooks yet.
Do not create static portfolio site yet.
Do not hand work to Copilot yet.
Stop after Wave 5 and provide the completion report.
