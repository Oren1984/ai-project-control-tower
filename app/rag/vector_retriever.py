from __future__ import annotations

from dataclasses import dataclass

from app.core.logging import get_logger
from app.rag.chunker import Chunk
from app.rag.embedding_provider import EmbeddingProvider

logger = get_logger(__name__)


@dataclass
class RetrievalResult:
    chunk_index: int
    source_path: str
    text: str
    score: float
    content_hash: str
    retrieval_method: str = "vector"


class VectorRetriever:
    """In-memory cosine-similarity retrieval using pgvector embeddings.
    Skipped gracefully when no embedding provider is available."""

    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self._provider = embedding_provider
        self._chunks: list[Chunk] = []
        self._embeddings: list[list[float]] = []

    def index(self, chunks: list[Chunk]) -> None:
        if not self._provider.is_available:
            logger.info("vector_retriever_skip", reason="embedding provider unavailable")
            return

        self._chunks = list(chunks)
        if self._chunks:
            self._embeddings = self._provider.embed([c.text for c in self._chunks])
        logger.info("vector_retriever_indexed", chunks=len(self._chunks))

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        if not self._provider.is_available or not self._chunks:
            return []

        import numpy as np

        query_emb = np.array(self._provider.embed([query])[0])
        q_norm = float(np.linalg.norm(query_emb))
        if q_norm == 0.0:
            return []

        scores: list[float] = []
        for emb in self._embeddings:
            e = np.array(emb)
            e_norm = float(np.linalg.norm(e))
            if e_norm == 0.0:
                scores.append(0.0)
            else:
                scores.append(float(np.dot(query_emb, e) / (q_norm * e_norm)))

        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [
            RetrievalResult(
                chunk_index=self._chunks[i].chunk_index,
                source_path=self._chunks[i].source_path,
                text=self._chunks[i].text,
                score=scores[i],
                content_hash=self._chunks[i].content_hash,
            )
            for i in top_indices
            if scores[i] > 0.0
        ]

    @property
    def is_available(self) -> bool:
        return self._provider.is_available
