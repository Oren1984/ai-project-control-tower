# Observability — AI Project Control Tower

## Overview

The system exposes:
- **Structured JSON logs** via structlog
- **Prometheus metrics** via `/metrics`
- **Grafana dashboard** pre-provisioned for the local stack
- **Request IDs** on every HTTP response (`X-Request-ID` header)

---

## Structured Logging

All log output is JSON-formatted using structlog.

Every log entry includes:
- `timestamp` (ISO 8601)
- `level`
- `logger` (module name)
- `request_id` (bound per HTTP request via middleware)
- Additional context fields (`audit_run_id`, `agent_name`, etc.)

### Example log line

```json
{
  "timestamp": "2026-05-02T10:00:00.000Z",
  "level": "info",
  "logger": "app.audit.audit_engine",
  "event": "audit_started",
  "request_id": "a1b2c3d4-...",
  "audit_run_id": 42,
  "mode": "hybrid"
}
```

### Log level

Set `LOG_LEVEL` in `.env`. Defaults to `INFO`.

---

## Prometheus Metrics

Endpoint: `GET /metrics`

### Available Metrics

| Metric | Type | Labels | Description |
|---|---|---|---|
| `audit_runs_total` | Counter | `mode` | Audit runs started |
| `audit_runs_failed_total` | Counter | — | Failed audit runs |
| `audit_duration_seconds` | Histogram | — | Wall-clock audit duration |
| `files_scanned_total` | Counter | — | Files scanned |
| `findings_total` | Counter | `severity` | Findings emitted |
| `rag_queries_total` | Counter | — | RAG retrieval queries |
| `rag_retrieval_latency_seconds` | Histogram | — | RAG retrieval latency |
| `agent_reviews_total` | Counter | `agent_name` | Agent reviews executed |
| `agent_review_duration_seconds` | Histogram | `agent_name` | Agent review duration |
| `report_generation_total` | Counter | `format` | Reports generated |
| `api_request_duration_seconds` | Histogram | `method`, `endpoint`, `status` | HTTP request duration |
| `db_query_errors_total` | Counter | — | Database query errors |

---

## Prometheus Configuration

`observability/prometheus/prometheus.yml` scrapes the API every 15 seconds:

```yaml
scrape_configs:
  - job_name: control-tower-api
    static_configs:
      - targets: [api:8000]
    metrics_path: /metrics
```

Access Prometheus at: http://localhost:9092

---

## Grafana Dashboard

Pre-provisioned dashboard: **AI Project Control Tower**

Access at: http://localhost:3012 (admin / admin by default)

Panels:
- Audit Runs Total (stat)
- Audit Runs Failed (stat)
- Files Scanned Total (stat)
- RAG Queries Total (stat)
- Audit Duration (p50 / p95 / p99 — timeseries)
- API Request Duration p95 by endpoint (timeseries)
- Findings by Severity rate (timeseries)
- RAG Retrieval Latency p95 (timeseries)
- Agent Reviews rate by agent (timeseries)

The dashboard auto-refreshes every 30 seconds.

---

## Request IDs

Every HTTP response includes an `X-Request-ID` header with a UUID v4.

This ID is bound to structlog context for the duration of the request, so all log entries from a single request share the same `request_id`.

---

## Viewing Logs

```bash
# API logs (structured JSON)
docker compose logs api --follow

# Parse with jq
docker compose logs api --follow | grep '^{' | jq .
```
