# API Reference — AI Project Control Tower

Base URL: `http://localhost:8013/api/v1`

All responses are JSON. All audit endpoints require a running PostgreSQL database.

---

## Health

### `GET /api/v1/health`

Liveness check. Returns 200 regardless of database state.

**Response**
```json
{"status": "ok", "service": "ai-project-control-tower"}
```

---

### `GET /api/v1/ready`

Readiness check. Validates database connectivity and pgvector extension.

**Response 200** (all checks pass)
```json
{
  "status": "ready",
  "checks": {"database": "ok", "pgvector": "ok"}
}
```

**Response 503** (any check fails)
```json
{
  "status": "not_ready",
  "checks": {"database": "error", "pgvector": "unknown"}
}
```

---

## Observability

### `GET /metrics`

Prometheus metrics exposition. Not shown in OpenAPI docs.

**Content-Type:** `text/plain; version=0.0.4`

---

## Projects

### `POST /api/v1/projects`

Create a project record.

**Body**
```json
{"name": "My AI Project", "description": "Optional description"}
```

**Response 201**
```json
{"id": 1, "name": "My AI Project", "description": "...", "created_at": "..."}
```

---

### `GET /api/v1/projects`

List all projects.

---

### `GET /api/v1/projects/{project_id}`

Get a single project by ID.

---

## Blueprints

### `POST /api/v1/blueprints`

Upload a Blueprint document (Markdown or plain text).

**Body**
```json
{
  "project_id": 1,
  "name": "AI System Blueprint v1",
  "content": "# Blueprint\n..."
}
```

---

### `GET /api/v1/blueprints/{blueprint_id}`

Get a blueprint by ID.

---

## Audits

### `POST /api/v1/audits/run`

Start a full audit run.

**Body**
```json
{
  "project_id": 1,
  "blueprint_id": 1,
  "repo_path": "/absolute/path/to/target/repo",
  "mode": "hybrid"
}
```

`mode` options: `rag_only` | `agent_only` | `hybrid`

**Response 201** — `AuditResult` object with findings, scores, and agent results.

> Note: The target repository must be under `ALLOWED_SCAN_PATHS`. The scan is read-only.

---

### `GET /api/v1/audits/history`

List recent audit runs (default last 20).

Query params: `limit` (1–100)

---

### `GET /api/v1/audits/{audit_run_id}`

Get a single audit run with summary.

---

### `GET /api/v1/audits/{audit_run_id}/findings`

Get all findings for an audit run.

---

### `GET /api/v1/audits/{audit_run_id}/report`

Get or generate a report for a completed audit run.

Query params: `format` — `markdown` (default) | `json` | `html`

**Response**
```json
{
  "audit_run_id": 1,
  "format": "markdown",
  "content": "# Audit Report\n...",
  "report_id": 1,
  "created_at": "2026-05-02T10:00:00Z"
}
```

---

## Error Responses

| Status | Meaning |
|---|---|
| 400 | Bad request (e.g., audit not completed yet) |
| 404 | Resource not found |
| 422 | Validation error (invalid body) |
| 500 | Internal server error |

All errors return: `{"detail": "error message"}`

---

## OpenAPI Docs

Interactive docs available at `http://localhost:8013/docs` when the API is running.
