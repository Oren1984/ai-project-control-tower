from pathlib import Path

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class PathValidationError(Exception):
    pass


def validate_scan_path(requested_path: str) -> Path:
    """
    Resolve to canonical absolute path and verify it falls within an allowed scan path.
    Resolving first naturally blocks path traversal (e.g. ../../) attempts.
    """
    allowed_paths = settings.allowed_scan_paths

    if not allowed_paths:
        raise PathValidationError(
            "No allowed scan paths configured. Set ALLOWED_SCAN_PATHS in environment."
        )

    try:
        resolved = Path(requested_path).resolve()
    except Exception as exc:
        raise PathValidationError(f"Cannot resolve path '{requested_path}': {exc}") from exc

    if not resolved.exists():
        raise PathValidationError(f"Path does not exist: {resolved}")

    if not resolved.is_dir():
        raise PathValidationError(f"Path is not a directory: {resolved}")

    for allowed_raw in allowed_paths:
        try:
            allowed_resolved = Path(allowed_raw).resolve()
            resolved.relative_to(allowed_resolved)
            logger.debug("path_validated", path=str(resolved), allowed=str(allowed_resolved))
            return resolved
        except ValueError:
            continue

    raise PathValidationError(
        f"Path '{resolved}' is outside all allowed scan paths. Allowed: {allowed_paths}"
    )
