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


# Wave 4 Prompt — Report Generator + Streamlit UI

Execute **Wave 4 only**.

Wave 1, Wave 2, and Wave 3 must already exist and pass validation.

## Wave 4 Scope

Build the user-facing workflow:

```text
Report generator
Markdown / JSON / HTML exports
Report sanitizer
Report storage
Streamlit UI
API client for UI
Download buttons
Findings dashboard
Audit history view
```

## Report Generator

Required files:

```text
app/reports/
app/reports/report_generator.py
app/reports/report_sanitizer.py
app/reports/report_store.py
app/reports/templates/report.md.j2
app/reports/templates/report.html.j2
app/reports/report_schema.py
```

Required formats:

```text
Markdown
JSON
HTML
```

Markdown is the primary format.

Report must follow the 18-section structure defined in:

```text
Doces/04_AUDIT_REPORT_TEMPLATE.md
```

## Report Safety

Before writing any report:

```text
Run report sanitizer
Mask secrets
Remove provider keys
Remove raw .env values
Do not include auto-fix instructions
Do not include patch/diff/code rewrite content
```

## Streamlit UI

Use Streamlit only.

Do not add React.

Required structure:

```text
ui/
ui/main.py
ui/pages/
ui/pages/page_project_setup.py
ui/pages/page_blueprint_upload.py
ui/pages/page_audit_mode.py
ui/pages/page_repository_scan.py
ui/pages/page_findings_dashboard.py
ui/pages/page_scores.py
ui/pages/page_final_report.py
ui/pages/page_audit_history.py
ui/pages/page_settings.py
ui/services/api_client.py
ui/components/
Dockerfile.ui
```

## UI Rules

The UI must:

```text
Communicate only through FastAPI
Never access DB directly
Never scan the target repository directly
Never write into target repositories
Use masked provider inputs
Show findings clearly
Allow report downloads
Show current audit history
```

## UI Pages

Implement:

```text
Project Setup
Blueprint Upload / Select
Audit Mode
Repository Scan
Findings Dashboard
Scores
Final Report
Audit History
Settings / Providers
```

## API

Add or complete API endpoints required by the UI:

```text
POST /api/v1/projects
POST /api/v1/blueprints
POST /api/v1/audits/run
GET /api/v1/audits/{id}
GET /api/v1/audits/{id}/findings
GET /api/v1/audits/{id}/report
GET /api/v1/audits/history
```

Keep routes thin.
Business logic belongs in services/audit/report modules.

## Tests

Add tests for:

```text
Report generation markdown
Report generation JSON
Report generation HTML
Report sanitizer
API report endpoint
UI API client helpers where practical
Basic Streamlit smoke structure if practical
No secrets in reports
No target repo modification after report generation
```

## Docker

Update Docker Compose to include the UI service if appropriate.

Services may include:

```text
api
ui
db
```

Do not add Prometheus/Grafana yet unless already trivial and isolated.

## End Requirement

Do not perform full final documentation polish yet.
Do not create notebooks or static site yet.
Stop after Wave 4 and provide the completion report.
