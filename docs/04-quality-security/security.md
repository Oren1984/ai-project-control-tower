# Security — AI Project Control Tower

## Core Safety Principle

**This system never modifies a target repository.**

This is enforced at multiple layers and validated by a mandatory E2E test that is a release gate.

---

## Guardrails

### 1. Path Allowlist

Only directories explicitly listed in `ALLOWED_SCAN_PATHS` may be scanned.

```bash
# .env
ALLOWED_SCAN_PATHS=["/home/user/projects", "/tmp/audits"]
```

Requests to scan paths outside the allowlist are rejected with a `PathValidationError` before any file is read.

### 2. Path Traversal Prevention

All requested scan paths are resolved with `Path.resolve()` before comparison against the allowlist. `../` traversal attacks are blocked automatically.

```
# Example: blocked
/allowed/path/../../secret  →  resolved → /secret  →  rejected
```

### 3. Binary File Skipping

Files that fail UTF-8 decoding are classified as binary and skipped entirely. Binary content is never read into memory for processing.

### 4. Oversized File Skipping

Files larger than `MAX_SCAN_FILE_SIZE_BYTES` (default: 1 MB) are skipped. This prevents memory exhaustion on repositories with large assets.

### 5. Secret Masking

The `SecretMasker` applies regex patterns to mask secrets before they appear in:
- Log output
- Findings
- Reports

Patterns masked:
- AWS access keys and secret keys
- OpenAI API keys (`sk-...`)
- Generic `PASSWORD=`, `SECRET=`, `API_KEY=`, `TOKEN=` patterns
- Bearer tokens

### 6. Report Sanitization

Before a report is stored or returned, the `ReportSanitizer` removes:
- `diff` and `patch` code blocks (no fix instructions in output)
- `## Auto Fix` sections
- Any residual secrets not caught by the masker

This enforces the **Recommendation Only** rule in output artifacts.

### 7. No Target Code Execution

The scanner reads file content as text. It never imports, executes, or evaluates code from the target repository.

### 8. No Auto-Fix

Findings contain a `recommendation` field (a single sentence). The system never generates step-by-step fix plans, patches, or diffs.

### 9. CORS

The API restricts CORS to configured origins (`cors_allowed_origins` in settings). Default: Streamlit UI at port 8513.

### 10. Provider Key Protection

LLM provider API keys (OpenAI, Anthropic, etc.) are loaded from environment variables and never logged. structlog processors strip them from log context.

---

## E2E Non-Modification Test

The mandatory release gate test in `tests/e2e/test_no_repo_modification.py` proves:

1. Every file SHA-256 hash is identical before and after the scan.
2. No new files were created.
3. No files were deleted.
4. File count is unchanged.

Run it with:
```bash
pytest tests/e2e/test_no_repo_modification.py -v
```

---

## Known Security Limitations

See [`known_limitations.md`](known_limitations.md) for the full list. Key items:
- No authentication on the API (local-only by design).
- No rate limiting on audit endpoints.
- Allowlist enforcement only happens for the initial path; the scanner does not re-validate each individual file against the allowlist.
- Git submodule content is not scanned by default.
