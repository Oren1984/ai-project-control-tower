from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "ai-project-control-tower"}


@router.get("/ready")
async def ready() -> JSONResponse:
    checks: dict[str, str] = {}
    db = None

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:
        logger.error("database_check_failed", error=str(exc))
        checks["database"] = "error"
    finally:
        if db is not None:
            db.close()

    # pgvector check — only attempted if DB is reachable
    if checks.get("database") == "ok":
        db2 = None
        try:
            db2 = SessionLocal()
            row = db2.execute(
                text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            ).fetchone()
            checks["pgvector"] = "ok" if row else "not_installed"
        except Exception as exc:
            logger.error("pgvector_check_failed", error=str(exc))
            checks["pgvector"] = "error"
        finally:
            if db2 is not None:
                db2.close()
    else:
        checks["pgvector"] = "unknown"

    all_ok = all(v == "ok" for v in checks.values())
    return JSONResponse(
        content={"status": "ready" if all_ok else "not_ready", "checks": checks},
        status_code=200 if all_ok else 503,
    )
