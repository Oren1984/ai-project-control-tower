# Deployment Guide — AI Project Control Tower

## Local Stack (Docker Compose)

The recommended way to run the full system locally.

### Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin)
- Git

### Quick Start

```bash
# 1. Clone and enter the repository
git clone <repo-url>
cd ai-project-control-tower

# 2. Create environment file
cp .env.example .env
# Edit .env — set ALLOWED_SCAN_PATHS and any LLM provider keys

# 3. Build and start all services
docker compose up --build

# 4. Run database migrations (first time only)
docker compose exec api alembic upgrade head
```

### Services

| Service | Host Port | Container Port | Purpose |
|---|---|---|---|
| db | 5433 | 5432 | PostgreSQL 16 + pgvector |
| api | 8013 | 8000 | FastAPI backend |
| ui | 8513 | 8501 | Streamlit frontend |
| prometheus | 9092 | 9090 | Metrics scraping |
| grafana | 3012 | 3000 | Metrics dashboards |

> **Docker networking:** host ports are for browser access. Inside Docker Compose, the UI
> reaches the API at `http://api:8000` (internal container port), not `localhost:8013`.

### Accessing Services

| URL | Service |
|---|---|
| http://localhost:8513 | Streamlit UI |
| http://localhost:8013/docs | FastAPI OpenAPI docs |
| http://localhost:8013/api/v1/health | API health check |
| http://localhost:9092 | Prometheus |
| http://localhost:3012 | Grafana (admin / admin) |

---

## Environment Variables

See `.env.example` for a full list. Critical variables:

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | set by docker-compose |
| `ALLOWED_SCAN_PATHS` | JSON array of allowed scan directories | `[]` |
| `MAX_SCAN_FILE_SIZE_BYTES` | Max file size to scan | `1048576` (1 MB) |
| `LOG_LEVEL` | Logging level | `INFO` |
| `GRAFANA_ADMIN_PASSWORD` | Grafana admin password | `admin` |

### Setting ALLOWED_SCAN_PATHS

```bash
# In .env — JSON array format
ALLOWED_SCAN_PATHS=["/home/user/projects", "/tmp/audits"]

# Or comma-separated
ALLOWED_SCAN_PATHS=/home/user/projects,/tmp/audits
```

---

## Database Migrations

```bash
# Apply all pending migrations
docker compose exec api alembic upgrade head

# Check migration history
docker compose exec api alembic history

# Downgrade one step
docker compose exec api alembic downgrade -1
```

---

## Useful Commands

```bash
# View logs for a specific service
docker compose logs api --follow

# Restart just the API
docker compose restart api

# Stop everything
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v

# Open a psql shell
docker compose exec db psql -U control_tower -d control_tower_db
```

---

## Stopping and Starting

```bash
# Stop all containers (data persists in volumes)
docker compose stop

# Start again
docker compose start
```

---

## Production Considerations

This system is local-first by design. For production deployment:

- Replace `docker compose` with Kubernetes or a managed container platform.
- Use a managed PostgreSQL instance (e.g., RDS, Cloud SQL) with pgvector support.
- Set strong passwords for all services.
- Restrict `ALLOWED_SCAN_PATHS` to a dedicated mount point.
- Use a reverse proxy (nginx/caddy) in front of FastAPI and Streamlit.
- Enable TLS.
- Store secrets in a vault (HashiCorp Vault, AWS Secrets Manager, etc.).

See `docs/known_limitations.md` for current limitations.
