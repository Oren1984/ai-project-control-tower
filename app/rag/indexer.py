from __future__ import annotations

from pathlib import Path

from app.core.logging import get_logger
from app.rag.chunker import Chunk, chunk_text
from app.schemas.scan_schemas import ScanResult

logger = get_logger(__name__)


class DocumentIndexer:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def index_scan_result(self, scan_result: ScanResult) -> list[Chunk]:
        all_chunks: list[Chunk] = []

        for scanned_file in scan_result.files:
            file_path = Path(scanned_file.path)
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                logger.warning("indexer_read_error", path=scanned_file.path, error=str(exc))
                continue

            chunks = chunk_text(
                text=text,
                source_path=scanned_file.relative_path,
                chunk_size=self.chunk_size,
                overlap=self.overlap,
            )
            all_chunks.extend(chunks)

        logger.info(
            "indexer_complete",
            files_indexed=len(scan_result.files),
            total_chunks=len(all_chunks),
        )
        return all_chunks

    def index_file(self, file_path: Path, relative_path: str = "") -> list[Chunk]:
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.warning("indexer_read_error", path=str(file_path), error=str(exc))
            return []

        return chunk_text(
            text=text,
            source_path=relative_path or str(file_path),
            chunk_size=self.chunk_size,
            overlap=self.overlap,
        )
