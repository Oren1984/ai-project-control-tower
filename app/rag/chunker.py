from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass
class Chunk:
    text: str
    source_path: str
    content_hash: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: dict = field(default_factory=dict)


def chunk_text(
    text: str,
    source_path: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[Chunk]:
    if not text.strip():
        return []

    content_hash = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    chunks: list[Chunk] = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(
            Chunk(
                text=text[start:end],
                source_path=source_path,
                content_hash=content_hash,
                chunk_index=chunk_index,
                start_char=start,
                end_char=end,
            )
        )
        chunk_index += 1
        if end == len(text):
            break
        start = end - overlap

    return chunks
