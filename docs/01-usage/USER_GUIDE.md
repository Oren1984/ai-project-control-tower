# AI Project Control Tower — User Guide

**Audience:** Technical users, recruiters, instructors, and future maintainers.

---

## What Is the AI Project Control Tower?

The AI Project Control Tower is a **read-only audit and governance system** for AI and software repositories. You give it a repository path and an architecture Blueprint document, and it:

1. Scans the repository files (read-only, no modifications ever)
2. Evaluates the repository against the Blueprint using a hybrid RAG pipeline and 7 specialist AI agents
3. Produces structured findings with severity levels and evidence
4. Scores the repository across 8 dimensions (0–100 per dimension + overall)
5. Generates a downloadable report in Markdown, HTML, or JSON

**The system never modifies any file in an inspected repository. This is a hard invariant.**

---

## The Full Workflow at a Glance

```
Project Setup → Blueprint Upload/Select → Audit Mode → Repository Scan
                                                              ↓
Final Report ← Audit History ← Scores ← Findings Dashboard
```

The UI is a 9-page Streamlit application at **http://localhost:8513**.

---

## Step 1 — Project Setup

**Page:** `Project Setup` (sidebar, top)

This is always your starting point. A Project represents the repository you want to audit.

### Create a new project

1. Fill in **Project Name** — a short label (e.g., `investment-mcp-multi-agent-system`)
2. Fill in **Local Repository Path** — enter the **container path** (see Docker Paths section below)
3. Optionally add a **Repository URL** (e.g., GitHub link for reference)
4. Optionally add a **Description**
5. Click **Create Project**

On success, the project is saved and automatically selected for the current session.

### Select an existing project

If you have already created projects, they appear in the **Existing Projects** list below the form. Click **Select** next to the project you want to work with.

> The selected project carries through to all subsequent pages via session state.

---

## Step 2 — Blueprint Upload / Select

**Page:** `Blueprint Upload / Select`

A Blueprint is a markdown or text document describing the desired architecture, conventions, and standards for the project you are auditing. The system compares the actual repository against this Blueprint.

### Register a new blueprint

1. Enter a **Blueprint Name** (e.g., `v1.0 Architecture Blueprint`)
2. Enter the **Blueprint File Path on the server** — this is the container path to the blueprint file (e.g., `/workspace/my-blueprints/arch_spec.md`)
3. Click **Register Blueprint**

### Select an existing blueprint

Registered blueprints for the current project appear in the **Available Blueprints** list. Click **Select** to attach a blueprint to the current session.

> If you do not have a blueprint file yet, you can paste your architecture specification into a `.md` file, place it in your mounted host directory, and reference it via its container path.

---

## Step 3 — Audit Mode

**Page:** `Audit Mode`

Choose how the audit engine should analyze the repository.

### Audit Mode options

| Mode | Description |
|---|---|
| **Hybrid (RAG + Agents)** | Recommended. Combines retrieval (TF-IDF + pgvector) with 7 specialist agents for the most thorough audit. |
| **Agent Only** | Skips retrieval; agents reason directly. Useful when embeddings are not configured. |
| **RAG Only** | Retrieval-based matching only, no agent reasoning. Faster but less detailed. |

### Retrieval Mode options

| Mode | Description |
|---|---|
| **hybrid** | Combines TF-IDF (keyword) and pgvector (semantic) results using Reciprocal Rank Fusion. |
| **tfidf** | Keyword-based retrieval only. Works without an embedding provider configured. |
| **pgvector** | Semantic vector search only. Requires an embedding provider API key. |

### Severity Threshold

Sets the minimum severity level for findings to include in results:
- `info` — include everything (default)
- `low`, `medium`, `high`, `critical` — progressively filter out lower-severity findings

Click **Save Settings** to persist the selections for this session.

---

## Step 4 — Repository Scan

**Page:** `Repository Scan`

This page runs the actual audit. Before clicking **Run Audit**, confirm the displayed Project, Audit Mode, and Blueprint are correct.

### Docker Paths — Critical

The API runs inside a Docker container. You **must enter the container path**, not the Windows host path.

The volume mount maps your Windows `C:\Users\ORENS` directory to `/workspace` inside the container.

| Windows host path | Enter this in the path field |
|---|---|
| `C:\Users\ORENS\investment-mcp-multi-agent-system` | `/workspace/investment-mcp-multi-agent-system` |
| `C:\Users\ORENS\rag-retrieval-evaluation-lab` | `/workspace/rag-retrieval-evaluation-lab` |
| `C:\Users\ORENS\ai-project-control-tower` *(this app itself)* | `/app` |

**Rule:** Strip `C:\Users\ORENS` and replace it with `/workspace`.

If you enter a Windows path such as `C:\Users\ORENS\...` in the field, the API will reject it with a path validation error because the container has no drive letters.

### Running the audit

1. Enter the **container path** to the target repository
2. Click **Run Audit**
3. Wait for the spinner to complete (typically 30 seconds to a few minutes depending on repository size and audit mode)
4. On success, the audit ID is saved to the session and you can navigate to Findings, Scores, History, and Report

---

## Step 5 — Findings Dashboard

**Page:** `Findings Dashboard`

Displays all findings from the most recent audit run.

### Severity counts (top row)

| Color | Severity | Meaning |
|---|---|---|
| 🔴 Red | Critical | Serious architectural or security gap; requires immediate attention |
| 🟠 Orange | High | Significant issue that should be addressed soon |
| 🟡 Yellow | Medium | Moderate issue; review and plan a fix |
| 🟢 Green | Low | Minor issue or best-practice deviation |
| ⚪ White | Info | Informational observation; no action required |

### Filtering findings

- **Filter by severity** — show only findings at or above a chosen level
- **Filter by agent** — show only findings from a specific specialist agent (Architecture, RAG/AI, DevOps, QA, Security, Documentation, Orchestrator)

### Reading a finding

Each finding card shows:
- **Title** — short description of the finding
- **Severity** — level indicator
- **Agent** — which specialist agent raised it
- **Evidence** — the specific file(s) or code patterns that triggered the finding
- **Recommendation** — a human-readable observation (note: the system never produces or applies automatic fixes)

---

## Step 6 — Scores

**Page:** `Scores`

Shows the 9-dimension scoring breakdown for the completed audit.

### Score dimensions

| Dimension | What is evaluated |
|---|---|
| Architecture | Structure, separation of concerns, module organisation |
| QA / Testing | Test coverage, test types, CI gates |
| Security | Secrets management, input validation, auth patterns |
| DevOps | Docker, CI/CD, environment configuration |
| MLOps | Model lifecycle, experiment tracking, data pipelines |
| Documentation | README, API docs, architecture docs, inline documentation |
| RAG / Agents | RAG pipeline design, agent structure, prompt quality |
| Observability | Logging, metrics, tracing, dashboards |

An **Overall Score** (0–100) is computed as a weighted average of all dimensions.

### Score interpretation

| Range | Meaning |
|---|---|
| 80–100 | Strong implementation; meets or exceeds blueprint standards |
| 60–79 | Acceptable; some gaps worth addressing |
| 40–59 | Moderate gaps; significant work needed |
| 0–39 | Significant issues; substantial rework required |

### Score N/A

If a dimension shows **N/A** or `0`, it means:
- The audit ran in a mode that did not evaluate that dimension (e.g., `rag_only` skips agent-based dimensions)
- The repository does not contain files relevant to that dimension
- No LLM provider key is configured and the deterministic stub returned no score for that dimension

N/A scores are not failures; they indicate the dimension was not assessable in the current run configuration.

---

## Step 7 — Audit History

**Page:** `Audit History`

Lists all audit runs recorded in the database for the current project (or all projects if no project is selected).

Each row shows:
- Audit ID
- Project name
- Status (`completed`, `failed`, `running`)
- Timestamp
- Overall score (if available)

Click **Select** on any past audit to load it as the active session — its findings, scores, and report become available across all pages.

### Failed audits

A `failed` status means the audit engine encountered an error during processing. Common causes:
- The repository path was not accessible inside the container (wrong path, volume not mounted)
- A required service (database, API) was unreachable
- An LLM provider call failed

The finding and score pages will show empty results for a failed audit. Check `docker compose logs api` for the error details, correct the path or configuration, and re-run the audit.

---

## Step 8 — Final Report

**Page:** `Final Report`

Generates and downloads a full audit report for the selected audit.

### Available formats

| Format | Use case |
|---|---|
| **Markdown** | Human-readable text; paste into GitHub, Notion, or a PR description |
| **HTML** | Standalone rendered report; open in a browser or send by email |
| **JSON** | Machine-readable; integrate with other tooling or parse programmatically |

Click **Generate Report** to produce the report, then use the **Download** button for the desired format.

Each report includes:
- Audit metadata (project, date, mode, status)
- Overall and per-dimension scores
- All findings with severity, evidence, and agent attribution
- A sanitised recommendations section (no patch instructions, no auto-fix content)

---

## Demo Mode

If you do not have a running backend, toggle **Demo Mode** in the sidebar. Demo Mode pre-populates all 9 pages with realistic static sample data:
- 1 project, 1 blueprint, 10 findings (critical through info)
- 9-dimension scores (overall 72/100)
- 3 audit history records
- Full Markdown, HTML, and JSON reports

Demo Mode is useful for walkthroughs, presentations, and exploring the UI without Docker.

---

## Settings Page

**Page:** `Settings`

Displays the current API connection status and session configuration. Useful for verifying that the UI is correctly connected to the backend.

---

## What the System Can and Cannot Do

### Can do

- Scan any repository path that is mounted into the container and listed in `ALLOWED_SCAN_PATHS`
- Evaluate code, configuration, documentation, and infrastructure files against a Blueprint
- Produce scored, evidence-backed findings across 8 technical dimensions
- Generate downloadable reports in three formats
- Run without LLM keys (deterministic stub mode)
- Operate entirely locally with no external data transmission (when using stub mode)

### Cannot do

- Modify, create, delete, or rename any file in a scanned repository (by design)
- Apply fixes or generate patch instructions
- Scan repositories that are not mounted into the container
- Run audits in parallel (one at a time)
- Authenticate users (no auth layer; intended for local/internal use)
- Rate-limit requests (no rate limiter configured)

---

## Known Limitations

| Limitation | Notes |
|---|---|
| Static read-only audit | The scanner reads files as text; it does not run or import the target code |
| No automatic code changes | Findings are observations only; remediation is always a human decision |
| Heuristic scores | Scores are produced by AI agents using heuristic reasoning, not formal verification |
| Some findings require human review | Agent findings may have false positives, especially for domain-specific code |
| LLM output quality depends on provider key | Without API keys, agents run in deterministic stub mode (limited depth) |
| pgvector semantic search requires embeddings | Without an embedding key, only TF-IDF retrieval is active |
| Jupyter notebooks parsed as raw JSON | Code cells are read as text, not executed |
| No authentication layer | Intended for local/private use only |
| Synchronous audits | One audit at a time; concurrent requests queue |

---

## Quick Reference: Page Order

| Step | Page | What you do |
|---|---|---|
| 1 | Project Setup | Create or select the project to audit |
| 2 | Blueprint Upload / Select | Register or select the blueprint document |
| 3 | Audit Mode | Choose audit mode, retrieval mode, severity threshold |
| 4 | Repository Scan | Enter container path and click Run Audit |
| 5 | Findings Dashboard | Review all findings by severity and agent |
| 6 | Scores | Read dimension and overall scores |
| 7 | Audit History | Browse past audits; reload a previous result |
| 8 | Final Report | Generate and download the full report |
| 9 | Settings | Check API connection status |
