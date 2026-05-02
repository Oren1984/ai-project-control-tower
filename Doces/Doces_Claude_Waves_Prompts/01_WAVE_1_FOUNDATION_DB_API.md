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


# Wave 1 Prompt — Foundation + DB + FastAPI Skeleton

Execute **Wave 1 only**.

## Wave 1 Scope

Build the project foundation:

```text
Foundation
FastAPI backend skeleton
PostgreSQL + pgvector
SQLAlchemy
Alembic
Pydantic settings
Basic structured logging
Docker Compose
Health endpoint
Ready endpoint
Minimal tests
Basic README update
CLAUDE.md engineering contract
```

## Do Not Build Yet

Do not build:

```text
Repository scanner
RAG layer
Agents
Audit engine
Report generator
Streamlit UI
Prometheus/Grafana
Full test suite
Copilot workflow
Notebook generation
Static site
```

## Required Backend Structure

Create a clean backend structure:

```text
app/
app/main.py
app/core/
app/core/config.py
app/core/logging.py
app/api/
app/api/routes/
app/api/routes/health.py
app/db/
app/db/session.py
app/db/base.py
app/db/models/
```

## Database Requirements

Use PostgreSQL + pgvector from day one.

Required:

```text
docker-compose.yml
PostgreSQL pgvector image
DATABASE_URL in .env.example
SQLAlchemy connection setup
Alembic initialized
Initial migration enabling pgvector extension if practical
```

If enabling pgvector in Alembic requires manual handling, document exactly what was done and how to validate it.

## Models

Add only the minimum models required for Wave 1.

Preferred minimum:

```text
Project
Blueprint
AuditRun
```

Do not create the entire final schema if it makes Wave 1 too large.
If you decide to create the full schema, explain clearly why.

## API Endpoints

Implement:

```text
GET /api/v1/health
GET /api/v1/ready
```

`health` checks app liveness.

`ready` checks:

```text
DB connection
pgvector extension availability if possible
```

## Tests

Add minimal tests:

```text
Health endpoint test
Ready endpoint test
DB connection test if practical
```

## Documentation

Update README minimally:

```text
What the project is
Current Wave 1 status
How to run Docker Compose
How to call /api/v1/health
How to call /api/v1/ready
How to run tests
```

Create `CLAUDE.md` with the engineering contract:

```text
Doces is the source of truth.
No auto-fix.
No generate fix plan.
No inspected repo modification.
No target code execution.
No React.
No SQLite.
PostgreSQL + pgvector only.
Streamlit UI only.
```

## End Requirement

Do not continue to Wave 2.
Stop after Wave 1 and provide the completion report.
