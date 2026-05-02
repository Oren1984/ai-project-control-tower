# Wave 6 Draft Prompt — Copilot Validation + Claude Deliverables Split

Status: Draft for later use after Wave 5 is complete.

This wave is intentionally not final yet.  
It should be reviewed and adjusted after the real codebase exists.

## Goal

After Waves 1–5 are completed, split the final work between:

```text
GitHub Copilot:
Full validation, E2E checks, Docker build/run, test execution, small fixes.

Claude:
Notebooks, static site, final docs, portfolio-ready summaries.
```

## Copilot Intended Role

Copilot should focus on execution and validation, not architecture.

Expected Copilot tasks:

```text
Run docker compose build
Run docker compose up
Validate API health
Validate API ready
Run pytest
Run E2E non-modification test
Run report generation test
Check Streamlit UI startup
Fix small test failures
Fix typing issues
Fix lint issues
Fix small Docker/Compose wiring issues
Document exact commands and results
```

Copilot must not:

```text
Change architecture
Add React
Add SQLite
Add auto-fix
Add Generate Fix Plan
Change Doces
Change Project-Blueprint-System
Change AI-System-Templates-Library
Rewrite large modules
Invent new agents
```

## Claude Intended Role

Claude should focus on deliverables and presentation.

Expected Claude tasks:

```text
Create project notebooks if needed
Create static demo site
Create docs summary
Create architecture explanation
Create portfolio narrative
Create final README polish
Create known limitations summary
Create QA summary
Create E2E validation summary
Create screenshots/demo instructions if needed
```

Claude must not:

```text
Modify core code during docs phase unless explicitly requested
Add new features
Change safety rules
Add auto-fix
Add Generate Fix Plan
```

## Final Wave 6 Plan

To be finalized later after Wave 5 results are known.
