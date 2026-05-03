# AI Project Control Tower — Installation Guide

This guide covers only setup and running the project. For UI usage, see [../01-usage/USER_GUIDE.md](../01-usage/USER_GUIDE.md).

---

## Prerequisites

| Tool | Version | Notes |
|---|---|---|
| **Git** | Any recent version | For cloning the repository |
| **Docker Desktop** | 4.x or newer | Includes Docker Engine + Docker Compose v2 |
| **Docker Compose** | v2.x (`docker compose`) | Bundled with Docker Desktop |
| **Python** | 3.11+ | Only needed if running outside Docker (e.g., Demo Mode without containers) |

Python is **not** required for the full Docker stack. All application dependencies are installed inside the containers.

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-org/ai-project-control-tower.git
cd ai-project-control-tower
```

---

## 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` and set the required values.

### Required — `HOST_REPOS_PATH`

This is the most important variable for running repository scans. It tells Docker which host directory to mount as `/workspace` inside the containers.

```env
HOST_REPOS_PATH=C:/Users/ORENS
```

With this mapping, any repository under `C:\Users\ORENS` on the host becomes visible inside the container at `/workspace/<repo-name>`.

Example:
- Host: `C:\Users\ORENS\investment-mcp-multi-agent-system`
- Container: `/workspace/investment-mcp-multi-agent-system`

### Required — `ALLOWED_SCAN_PATHS`

Comma-separated or JSON list of container paths the scanner is permitted to read. This is a security allowlist; the scanner will reject any path not covered by it.

```env
ALLOWED_SCAN_PATHS=["/workspace","/app"]
```

- `/workspace` — covers all repositories mounted from `HOST_REPOS_PATH`
- `/app` — covers the control tower repo itself (if you want to audit it)

If this is left empty, the Docker Compose default `["/app","/workspace"]` is used.

### Optional — LLM Provider Keys

Without these, agents run in deterministic stub mode (no external calls, limited analysis depth).

```env
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
```

### Optional — Database

The defaults work out of the box with Docker Compose. Only change these if you are connecting to an external PostgreSQL instance.

```env
POSTGRES_USER=control_tower
POSTGRES_PASSWORD=control_tower_pass
POSTGRES_DB=control_tower_db
```

### Optional — Demo Mode

Start the UI in Demo Mode by default (no backend required, no API keys needed):

```env
DEMO_MODE=true
```

### Full `.env` example

```env
# Host path to mount as /workspace inside containers
HOST_REPOS_PATH=C:/Users/ORENS

# Scanner allowlist (container paths)
ALLOWED_SCAN_PATHS=["/workspace","/app"]

# Database (defaults work with Docker Compose)
POSTGRES_USER=control_tower
POSTGRES_PASSWORD=control_tower_pass
POSTGRES_DB=control_tower_db

# LLM provider (optional; omit to use deterministic stubs)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Demo Mode (optional)
DEMO_MODE=false

# Grafana admin password
GRAFANA_ADMIN_PASSWORD=admin
```

---

## 3. Volume Mapping for Repository Scanning

The `docker-compose.yml` mounts the host directory at `/workspace` in read-only mode:

```yaml
volumes:
  - ${HOST_REPOS_PATH:-/tmp/repos}:/workspace:ro
```

The `:ro` (read-only) flag is strongly recommended because:
- It enforces the system's core safety invariant at the OS level — the container literally cannot write to your repositories
- It prevents accidental file modification even if a bug bypasses application-level checks
- It makes the Docker Compose configuration self-documenting about intent

To scan repositories stored at `C:\Users\ORENS`, set in `.env`:

```env
HOST_REPOS_PATH=C:/Users/ORENS
```

**Important:** Use forward slashes on Windows in the `.env` file (`C:/Users/ORENS`, not `C:\Users\ORENS`). Docker Desktop on Windows requires forward slashes in volume source paths.

---

## 4. Build the Docker Images

```bash
docker compose build
```

This builds the FastAPI image (`Dockerfile`) and the Streamlit UI image (`Dockerfile.ui`). The `db`, `prometheus`, and `grafana` services use pre-built public images and do not need building.

---

## 5. Start the Stack

```bash
docker compose up
```

This starts all five services:
- `db` — PostgreSQL 16 + pgvector
- `api` — FastAPI backend
- `ui` — Streamlit UI
- `prometheus` — Metrics collection
- `grafana` — Dashboards

Add `-d` to run in the background:

```bash
docker compose up -d
```

On first run, `entrypoint.sh` automatically runs `alembic upgrade head` to apply database migrations before the API starts.

---

## 6. Open the UI

Once all containers are healthy, open your browser:

```
http://localhost:8513
```

---

## 7. Validate the Installation

### Check all containers are running

```bash
docker compose ps
```

All five services (`db`, `api`, `ui`, `prometheus`, `grafana`) should show status `Up` or `running`.

### Validate API health

```bash
curl http://localhost:8013/api/v1/health
```

Expected response:

```json
{"status": "ok"}
```

### Validate readiness (database connected)

```bash
curl http://localhost:8013/api/v1/ready
```

Expected response:

```json
{"status": "ready"}
```

### Validate that the UI connects to the API

1. Open http://localhost:8513
2. Navigate to the **Settings** page in the sidebar
3. The page should show a green API connection status

### Validate metrics endpoint

```bash
curl http://localhost:8013/metrics | head -20
```

Should return Prometheus metric lines.

### Service URLs

| URL | Service |
|---|---|
| http://localhost:8513 | Streamlit UI |
| http://localhost:8013/docs | FastAPI OpenAPI docs |
| http://localhost:8013/api/v1/health | API health check |
| http://localhost:8013/api/v1/ready | API readiness check |
| http://localhost:9092 | Prometheus |
| http://localhost:3012 | Grafana (admin / admin) |

---

## 8. Stop the Stack

```bash
docker compose down
```

To also remove the database volume (resets all stored data):

```bash
docker compose down -v
```

---

## Common Problems and Solutions

### Docker is not installed or not running

**Symptom:** `docker compose` command not found, or `Cannot connect to the Docker daemon`.

**Fix:** Install Docker Desktop from https://docs.docker.com/desktop/install/windows-install/ and start it before running any `docker compose` command.

---

### Wrong Windows path in `HOST_REPOS_PATH`

**Symptom:** Repository paths entered in the UI are rejected with a path validation error, or the API cannot find the repository.

**Fix:** In `.env`, use forward slashes: `HOST_REPOS_PATH=C:/Users/ORENS`. Do not use backslashes.

---

### Repository path not visible inside the container

**Symptom:** The audit fails with "path not allowed" or "directory does not exist".

**Checklist:**
1. `HOST_REPOS_PATH` in `.env` points to the correct parent directory on the host
2. The repository subdirectory actually exists under that path
3. In the UI, you entered the container path (`/workspace/repo-name`) not the Windows path
4. `ALLOWED_SCAN_PATHS` includes `/workspace`

---

### `ALLOWED_SCAN_PATHS` mismatch

**Symptom:** Scan fails with a path validation error even though the path exists inside the container.

**Fix:** Ensure `ALLOWED_SCAN_PATHS` in `.env` includes a prefix that covers the path you entered. For `/workspace/my-repo`, `ALLOWED_SCAN_PATHS` must include `/workspace` (not `/workspace/my-repo` specifically — prefix matching is used).

---

### API not reachable from the UI

**Symptom:** UI pages show connection errors or "Could not load projects".

**Fix:** The UI container contacts the API at `http://api:8000` (internal Docker network). This is set automatically. Verify with:

```bash
docker compose logs ui
docker compose logs api
```

If the `api` container failed to start (e.g., database not ready), restart the stack:

```bash
docker compose down
docker compose up
```

---

### `FATAL: database "control_tower" does not exist`

**Symptom:** API fails to start; `docker compose logs api` shows this error.

**Cause:** A stale Docker volume from a previous run has a different database name.

**Fix:**

```bash
docker compose down -v
docker compose up --build
```

Warning: `down -v` deletes all stored data (projects, blueprints, audit history). Use only when a clean start is acceptable.

---

### Port already in use

**Symptom:** `Bind for 0.0.0.0:8513 failed: port is already allocated` (or similar for other ports).

**Fix:** Stop whatever process is using the port, or change the host port in `docker-compose.yml`. The relevant host ports are `5433`, `8013`, `8513`, `9092`, `3012`.

---

## Troubleshooting Commands

```bash
# Check container status
docker compose ps

# View API logs (most useful for debugging audit failures)
docker compose logs api

# View UI logs
docker compose logs ui

# Follow live logs
docker compose logs -f api

# Stop and remove containers
docker compose down

# Rebuild images from scratch
docker compose build --no-cache

# Start fresh (removes stored data)
docker compose down -v
docker compose up --build
```
