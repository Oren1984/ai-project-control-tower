from fastapi import APIRouter, HTTPException

from app.core.logging import get_logger
from app.scanner.path_validator import PathValidationError, validate_scan_path
from app.scanner.repo_scanner import RepoScanner
from app.schemas.scan_schemas import ScanRequest, ScanResult

router = APIRouter()
logger = get_logger(__name__)


@router.post("/scans", response_model=ScanResult)
async def run_scan(request: ScanRequest) -> ScanResult:
    try:
        validated_path = validate_scan_path(request.repo_path)
    except PathValidationError as exc:
        logger.warning("scan_path_rejected", path=request.repo_path, reason=str(exc))
        raise HTTPException(status_code=400, detail=str(exc))

    scanner = RepoScanner(
        max_file_size_bytes=request.max_file_size_bytes,
        include_hidden=request.include_hidden,
        skip_git_internals=request.skip_git_internals,
        follow_symlinks=request.follow_symlinks,
    )

    try:
        result = scanner.scan(validated_path)
    except Exception as exc:
        logger.error("scan_failed", path=str(validated_path), error=str(exc))
        raise HTTPException(status_code=500, detail="Scan failed unexpectedly")

    return result
