from __future__ import annotations

from dataclasses import dataclass

from app.rag.chunker import Chunk
from app.rag.embedding_provider import EmbeddingProvider, NullEmbeddingProvider
from app.rag.tfidf_retriever import TFIDFRetriever
from app.rag.vector_retriever import VectorRetriever


@dataclass
class HybridResult:
    chunk_index: int
    source_path: str
    text: str
    score: float
    content_hash: str
    retrieval_method: str = "hybrid"


class HybridRetriever:
    """Merges TF-IDF and vector scores. Falls back to pure TF-IDF when embeddings unavailable."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider | None = None,
        tfidf_weight: float = 0.5,
        vector_weight: float = 0.5,
    ) -> None:
        self._embedding_provider = embedding_provider or NullEmbeddingProvider()
        self._tfidf = TFIDFRetriever()
        self._vector = VectorRetriever(embedding_provider=self._embedding_provider)
        self._tfidf_weight = tfidf_weight
        self._vector_weight = vector_weight

    def index(self, chunks: list[Chunk]) -> None:
        self._tfidf.index(chunks)
        self._vector.index(chunks)

    def retrieve(self, query: str, top_k: int = 5) -> list[HybridResult]:
        tfidf_results = self._tfidf.retrieve(query, top_k=top_k * 2)
        vector_results = self._vector.retrieve(query, top_k=top_k * 2)

        if not self._vector.is_available:
            return [
                HybridResult(
                    chunk_index=r.chunk_index,
                    source_path=r.source_path,
                    text=r.text,
                    score=r.score,
                    content_hash=r.content_hash,
                    retrieval_method="tfidf",
                )
                for r in tfidf_results[:top_k]
            ]

        combined: dict[int, float] = {}
        metadata: dict[int, tuple[str, str, str]] = {}

        for r in tfidf_results:
            combined[r.chunk_index] = combined.get(r.chunk_index, 0.0) + r.score * self._tfidf_weight
            metadata[r.chunk_index] = (r.source_path, r.text, r.content_hash)

        for r in vector_results:
            combined[r.chunk_index] = combined.get(r.chunk_index, 0.0) + r.score * self._vector_weight
            if r.chunk_index not in metadata:
                metadata[r.chunk_index] = (r.source_path, r.text, r.content_hash)

        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            HybridResult(
                chunk_index=ci,
                source_path=metadata[ci][0],
                text=metadata[ci][1],
                score=sc,
                content_hash=metadata[ci][2],
                retrieval_method="hybrid",
            )
            for ci, sc in ranked
            if ci in metadata
        ]

    @property
    def chunk_count(self) -> int:
        return self._tfidf.chunk_count
