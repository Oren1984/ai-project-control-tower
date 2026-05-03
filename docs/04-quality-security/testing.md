# Testing Guide — AI Project Control Tower

## Test Matrix

| Layer | Files | Notes |
|---|---|---|
| Unit — Scanner | `tests/unit/test_scanner.py` | File discovery, classification |
| Unit — Secret Masker | `tests/unit/test_secret_masker.py` | Pattern matching |
| Unit — Path Validator | `tests/unit/test_path_validator.py` | Allowlist, traversal |
| Unit — Chunker | `tests/test_chunker.py` | RAG text chunking |
| Unit — TF-IDF | `tests/test_tfidf_retriever.py` | Lexical retrieval |
| Unit — Hybrid Retriever | `tests/test_hybrid_retriever.py` | RRF fusion |
| Unit — Scoring | `tests/test_scoring.py` | Dimension scores |
| Unit — Audit Engine | `tests/test_audit_engine.py` | Engine logic |
| Unit — Agent Schemas | `tests/test_agent_schemas.py` | Pydantic models |
| Report Generation | `tests/test_report_generator.py` | Markdown / JSON / HTML |
| Report Sanitizer | `tests/test_report_sanitizer.py` | Secret removal, auto-fix removal |
| API | `tests/test_health.py` | Health + ready endpoints |
| API — Reports | `tests/test_api_report.py` | Report generation endpoints |
| Metrics | `tests/test_metrics.py` | Prometheus /metrics, request IDs |
| Security | `tests/test_security.py` | Path traversal, secret masking, read-only |
| Integration (DB) | `tests/integration/test_integration.py` | Live DB — skipped if not reachable |
| E2E — Non-Modification | `tests/e2e/test_no_repo_modification.py` | **Release gate** |

---

## Running Tests

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run all tests (no database required)

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=app --cov-report=term-missing
```

### Run a specific test file

```bash
pytest tests/e2e/test_no_repo_modification.py -v
pytest tests/test_security.py -v
```

### Run integration tests (requires live database)

```bash
docker compose up -d db
pytest tests/integration/ -v
```

---

## The E2E Non-Modification Test

The most important test in the suite. It is a **release gate** — the project must not ship if this test fails.

**What it proves:**
1. Every file's SHA-256 hash is identical before and after a full scan.
2. No new files were created by the scanner.
3. No files were deleted by the scanner.
4. File count is unchanged.
5. Scanner output is idempotent across multiple runs.

```bash
pytest tests/e2e/test_no_repo_modification.py -v
```

---

## Test Configuration

`pyproject.toml`:
```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
asyncio_mode = "auto"
```

---

## Adding New Tests

- Place unit tests in `tests/unit/` or `tests/` depending on scope.
- Integration tests (require DB) go in `tests/integration/` and must use the `requires_db` marker.
- E2E tests go in `tests/e2e/`.
- Do not mock the database in integration tests.
- Do not test that findings contain specific text — agent output is non-deterministic when using real LLMs.

---

## Known Test Limitations

- Integration tests are skipped automatically when no database is available.
- Agent output tests use mock/stub agents — real LLM calls are not exercised in the CI suite.
- There is no browser-based E2E test for the Streamlit UI.
