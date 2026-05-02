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


# Wave 2 Prompt — Repository Scanner + Security Guardrails

Execute **Wave 2 only**.

Wave 1 must already exist and pass basic validation.

## Wave 2 Scope

Build the read-only repository scanner and the first security guardrails.

Required modules:

```text
app/scanner/
app/scanner/repo_scanner.py
app/scanner/file_classifier.py
app/scanner/secret_masker.py
app/scanner/path_validator.py
app/schemas/scan_schemas.py
tests/unit/test_scanner.py
tests/unit/test_secret_masker.py
tests/unit/test_path_validator.py
tests/e2e/test_no_repo_modification.py
```

## Core Safety Contract

The scanner must be read-only.

It must:

```text
Read files
Analyze metadata
Build inventory
Mask secrets
Skip unsafe files
Never modify files
Never execute code
Never write into the inspected target repository
```

## Scanner Requirements

The scanner should:

```text
Scan recursively
Include hidden files
Ignore .git internals unless explicitly configured
Detect text vs binary files
Skip binary files safely
Apply max file size limit
Calculate sha256 file hashes
Collect file path, extension, size, modified time, type
Mask secrets before storing or returning content
Track skipped files and reasons
Handle encoding errors safely
Avoid following symlinks by default
```

## Path Validation Requirements

Implement an allowlist-based path validator.

Required behavior:

```text
ALLOWED_SCAN_PATHS from env
Resolve absolute canonical path
Reject paths outside allowlist
Reject path traversal attempts
Reject unsafe symlink traversal
Return clear validation errors
```

## Secret Masking Requirements

Mask at minimum:

```text
AWS access keys
AWS secret keys
GitHub tokens
Generic API keys
JWT-like tokens
.env style secrets
OpenAI / Anthropic / Google API keys
```

Use `[REDACTED]`.

Original secrets must not be stored, logged, or returned.

## Tests

Add focused tests for:

```text
Recursive scanning
Hidden file scanning
Binary skipping
Oversized file skipping
Hash generation
Secret masking
Path allowlist pass
Path allowlist fail
Path traversal block
Symlink safety if practical
```

## Mandatory E2E Safety Test

Create an early E2E non-modification test.

Flow:

```text
Copy a sample repo to a temp directory
Record sha256 hash of every file before scan
Run scanner
Record sha256 hash of every file after scan
Assert hashes are identical
Assert no files were added
Assert no files were deleted
Assert file count is unchanged
```

This test must remain part of the project until final release.

## API

Only add scanner API endpoints if they are necessary and small.

Optional endpoint:

```text
POST /api/v1/scans
```

If added, it must use path validation.

## End Requirement

Do not build RAG.
Do not build agents.
Do not build audit engine.
Stop after Wave 2 and provide the completion report.
