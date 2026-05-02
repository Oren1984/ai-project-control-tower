from __future__ import annotations

from dataclasses import dataclass

from app.rag.chunker import Chunk


@dataclass
class RetrievalResult:
    chunk_index: int
    source_path: str
    text: str
    score: float
    content_hash: str
    retrieval_method: str = "tfidf"


class TFIDFRetriever:
    """In-memory TF-IDF retrieval using scikit-learn. No external DB required."""

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []
        self._vectorizer = None
        self._matrix = None
        self._fitted = False

    def index(self, chunks: list[Chunk]) -> None:
        from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore

        self._chunks = list(chunks)
        if not self._chunks:
            return

        self._vectorizer = TfidfVectorizer(
            max_features=10_000,
            stop_words="english",
            ngram_range=(1, 2),
        )
        self._matrix = self._vectorizer.fit_transform([c.text for c in self._chunks])
        self._fitted = True

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        if not self._fitted or not self._chunks:
            return []

        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

        query_vec = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self._matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            if float(scores[idx]) > 0.0:
                chunk = self._chunks[int(idx)]
                results.append(
                    RetrievalResult(
                        chunk_index=chunk.chunk_index,
                        source_path=chunk.source_path,
                        text=chunk.text,
                        score=float(scores[idx]),
                        content_hash=chunk.content_hash,
                    )
                )
        return results

    @property
    def is_fitted(self) -> bool:
        return self._fitted

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)
