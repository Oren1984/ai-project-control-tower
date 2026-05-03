# AI Project Control Tower — Testing, Observability & Security Plan

## 1. Testing Philosophy

The project is not complete without a full test matrix.

Testing must prove:

- The scanner works.
- The RAG layer retrieves correctly.
- The agents return structured findings.
- The DB persists audit data.
- The API works.
- Reports are generated correctly.
- Secrets are protected.
- Target repositories are not modified.

---

## 2. Required Test Types

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

---

## 3. Scanner Tests

Verify:

- Recursive scanning
- Hidden file scanning
- File inventory generation
- Hash generation
- Binary file skipping
- File size limit behavior
- Safe error handling
- No modification of target files

---

## 4. RAG Tests

Verify:

- Chunking
- Overlap
- Metadata preservation
- TF-IDF retrieval
- pgvector retrieval
- Hybrid retrieval
- Empty index handling
- Missing embedding fallback

---

## 5. Agent Tests

Verify:

- Valid output schema
- Valid category
- Valid severity
- Recommendation exists
- Evidence exists when available
- No auto-fix output
- No file modifications
- Orchestrator merges results correctly

---

## 6. DB Tests

Verify:

- Projects table
- Blueprints table
- Audit runs table
- Findings table
- Reports table
- Knowledge sources
- Documents
- Document chunks
- Agent reviews
- Relationships
- Alembic migrations

---

## 7. API Tests

Required endpoint tests:

```text
GET  /api/v1/health
GET  /api/v1/ready
POST /api/v1/projects
POST /api/v1/audits/run
GET  /api/v1/audits/{id}
GET  /api/v1/audits/{id}/findings
GET  /api/v1/audits/{id}/report
```

---

## 8. E2E Test

Main E2E flow:

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

The final check is mandatory.

---

## 9. Observability Requirements

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

---

## 10. Health and Readiness

### Health

```text
GET /api/v1/health
```

Checks that the app is alive.

### Ready

```text
GET /api/v1/ready
```

Checks:

- DB connection
- pgvector availability
- Storage path writable
- Provider configuration
- RAG index availability if relevant

---

## 11. Security Requirements

Required:

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
Input validation
Path traversal prevention
Controlled CORS
Basic rate limiting
```

---

## 12. Security Testing

Security tests must verify:

- `.env` is not exposed in reports.
- API keys are masked.
- Hardcoded secrets are detected.
- Path traversal is blocked.
- Invalid repo paths are rejected.
- Binary files are skipped.
- Oversized files are skipped.
- The target repository is not modified.
- The system does not execute target project code.
