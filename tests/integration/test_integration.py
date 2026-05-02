"""
Integration tests — require a live database connection.

These tests are skipped automatically when DATABASE_URL points to an
unreachable server. Run against the Docker Compose stack:

    docker compose up -d db api
    pytest tests/integration/ -v
"""
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from app.core.config import settings


def _db_reachable() -> bool:
    try:
        engine = create_engine(settings.database_url, connect_args={}, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False


requires_db = pytest.mark.skipif(
    not _db_reachable(),
    reason="Live database not reachable — start Docker Compose stack first",
)


@requires_db
def test_database_connection():
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
    assert result == 1


@requires_db
def test_pgvector_extension_installed():
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        ).fetchone()
    assert row is not None, "pgvector extension is not installed"


@requires_db
def test_required_tables_exist():
    required = {
        "projects",
        "blueprints",
        "audit_runs",
        "findings",
        "rag_documents",
        "rag_document_chunks",
        "reports",
    }
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'public'"
            )
        ).fetchall()
    actual = {r[0] for r in rows}
    missing = required - actual
    assert not missing, f"Missing tables: {missing}"


@requires_db
def test_health_endpoint_ready_with_live_db(client):
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["checks"]["database"] == "ok"
    assert data["checks"]["pgvector"] == "ok"
