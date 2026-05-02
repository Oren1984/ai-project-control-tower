# Known Limitations — AI Project Control Tower

## Authentication and Authorization

The API has no authentication layer. It is designed for local use only. Do not expose port 8000 to a public network.

## Rate Limiting

There is no rate limiting on the audit endpoints. A long-running audit blocks the API process for its duration. For production use, add `slowapi` or move audits to a background worker queue (Celery, ARQ, etc.).

## LLM Provider Integration

Agents use a simple stub/mock by default. Real LLM integration (Claude, OpenAI, Gemini) requires provider API keys configured in `.env`. Without a real provider, agent findings are deterministic stubs, not real AI analysis.

## Embedding Provider

pgvector semantic search requires an embedding provider configured (`EMBEDDING_PROVIDER`). Without it, the system falls back to TF-IDF only. Hybrid retrieval requires a live embedding model.

## Audit Concurrency

Audit runs are synchronous. Running two audits simultaneously against the same API instance is not tested and may produce inconsistent results. One audit at a time is the supported usage pattern.

## Git Internals

The scanner skips `.git/` internals by default (`skip_git_internals=True`). Git history, stashes, and packed objects are not analysed.

## Git Submodules

Submodule content is not automatically traversed. Only the top-level repository files are scanned.

## Large Repositories

Files over `MAX_SCAN_FILE_SIZE_BYTES` (default 1 MB) are skipped. Repositories with many large files will have lower coverage. Binary assets (images, compiled artifacts, models) are skipped entirely.

## Report Formats

HTML reports are generated with Jinja2 and do not include interactive charts. For rich visualisations, export JSON and post-process externally.

## Streamlit UI State

The Streamlit UI uses session state. Refreshing the browser clears in-progress workflows. Completed audits are persisted in the database and can be accessed via the Audit History page.

## Database Schema Migrations

Schema changes require running `alembic upgrade head`. There is no automatic migration on startup. If you upgrade the application and skip migrations, the API will fail with a schema mismatch.

## No Notebook Support

Jupyter notebooks (`.ipynb`) are not parsed for code content. Only the raw JSON structure is scanned as text.

## No Static Site Export

There is no built-in export of reports to a static HTML site. This is planned for a future wave.

## Windows Path Handling

On Windows, paths use backslashes. The path validator normalises paths with `Path.resolve()`. Ensure `ALLOWED_SCAN_PATHS` uses forward slashes or raw Windows paths consistently.

## Prometheus Metrics Are In-Process Only

All Prometheus metrics are stored in the API process's memory. Restarting the API resets all counters to zero. Use Prometheus's remote write or a pushgateway for durability across restarts.
