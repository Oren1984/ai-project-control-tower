import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

from app.core.logging import get_logger
from app.scanner.file_classifier import classify_file
from app.schemas.scan_schemas import (
    FileType,
    ScannedFile,
    ScanResult,
    SkippedFile,
    SkipReason,
)

logger = get_logger(__name__)

_BINARY_CHECK_BYTES = 8192


def _is_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:_BINARY_CHECK_BYTES]
        return b"\x00" in chunk
    except OSError:
        return True


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
    except OSError:
        pass
    return h.hexdigest()


class RepoScanner:
    def __init__(
        self,
        max_file_size_bytes: int = 1_048_576,
        include_hidden: bool = True,
        skip_git_internals: bool = True,
        follow_symlinks: bool = False,
    ) -> None:
        self.max_file_size_bytes = max_file_size_bytes
        self.include_hidden = include_hidden
        self.skip_git_internals = skip_git_internals
        self.follow_symlinks = follow_symlinks

    def scan(self, repo_path: Path) -> ScanResult:
        files: list[ScannedFile] = []
        skipped: list[SkippedFile] = []

        for root, dirs, filenames in os.walk(str(repo_path), followlinks=self.follow_symlinks):
            root_path = Path(root)

            try:
                rel_root = root_path.relative_to(repo_path)
            except ValueError:
                rel_root = root_path

            # Prune .git in-place so os.walk never recurses into it
            if self.skip_git_internals:
                dirs[:] = [d for d in dirs if d != ".git"]

            # Prune hidden directories when include_hidden is False
            if not self.include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(".")]

            for filename in filenames:
                if not self.include_hidden and filename.startswith("."):
                    continue
                file_path = root_path / filename
                rel_path = rel_root / filename

                scanned, skip = self._process_file(file_path, rel_path, repo_path)
                if skip is not None:
                    skipped.append(skip)
                elif scanned is not None:
                    files.append(scanned)

        total = len(files) + len(skipped)
        logger.info(
            "scan_complete",
            repo_path=str(repo_path),
            scanned=len(files),
            skipped=len(skipped),
        )
        return ScanResult(
            repo_path=str(repo_path),
            scanned_at=datetime.now(timezone.utc),
            total_files_found=total,
            total_files_scanned=len(files),
            total_files_skipped=len(skipped),
            files=files,
            skipped=skipped,
        )

    def _process_file(
        self,
        file_path: Path,
        rel_path: Path,
        repo_root: Path,
    ) -> tuple[ScannedFile | None, SkippedFile | None]:
        str_path = str(file_path)
        str_rel = str(rel_path)

        # Symlink guard: never follow unless explicitly enabled
        if not self.follow_symlinks and file_path.is_symlink():
            return None, SkippedFile(
                path=str_path,
                relative_path=str_rel,
                reason=SkipReason.SYMLINK,
            )

        try:
            stat = file_path.stat()
        except OSError as exc:
            return None, SkippedFile(
                path=str_path,
                relative_path=str_rel,
                reason=SkipReason.ENCODING_ERROR,
                details=f"stat failed: {exc}",
            )

        size_bytes = stat.st_size
        modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

        if size_bytes > self.max_file_size_bytes:
            return None, SkippedFile(
                path=str_path,
                relative_path=str_rel,
                reason=SkipReason.OVERSIZED,
                details=f"{size_bytes} bytes exceeds limit of {self.max_file_size_bytes}",
            )

        if _is_binary(file_path):
            return None, SkippedFile(
                path=str_path,
                relative_path=str_rel,
                reason=SkipReason.BINARY,
            )

        sha = _sha256(file_path)
        is_hidden = file_path.name.startswith(".")
        category = classify_file(file_path, repo_root)

        return (
            ScannedFile(
                path=str_path,
                relative_path=str_rel,
                extension=file_path.suffix,
                size_bytes=size_bytes,
                modified_at=modified_at,
                file_type=FileType.TEXT,
                category=category,
                sha256=sha,
                is_hidden=is_hidden,
            ),
            None,
        )
