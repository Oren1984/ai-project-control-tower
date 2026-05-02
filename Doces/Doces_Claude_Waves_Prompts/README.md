# Claude Wave Prompts — AI Project Control Tower

Documentation folder name: `Doces`

This folder contains ready-to-use prompts for Claude Code.

## Prompt Order

```text
01_WAVE_1_FOUNDATION_DB_API.md
02_WAVE_2_SCANNER_SECURITY.md
03_WAVE_3_RAG_AGENTS_AUDIT_ENGINE.md
04_WAVE_4_REPORTS_STREAMLIT_UI.md
05_WAVE_5_TESTING_OBSERVABILITY_DOCS.md
06_DRAFT_COPILOT_CLAUDE_HANDOFF.md
```

## Usage Rule

Run one wave at a time.

Do not give Claude all waves for execution at once.

After each wave:

1. Review the completion report.
2. Run the validation commands.
3. Commit the changes.
4. Only then continue to the next wave.

## Main Safety Rule

This project is an audit and recommendation system only.

```text
Recommendation Only.
No Auto Fix.
No Generate Fix Plan.
No inspected repository modification.
No target project code execution.
```

## Division Later

After Wave 5, Wave 6 will be finalized:

```text
Copilot:
E2E validation, Docker build/run, test execution, small fixes.

Claude:
Notebooks, static site, final docs, project summaries.
```
