from __future__ import annotations

from app.core.logging import get_logger
from app.rag.chunker import Chunk
from app.rag.embedding_provider import EmbeddingProvider, get_embedding_provider
from app.rag.hybrid_retriever import HybridRetriever
from app.rag.indexer import DocumentIndexer
from app.rag.tfidf_retriever import TFIDFRetriever
from app.rag.vector_retriever import VectorRetriever
from app.schemas.scan_schemas import ScanResult

logger = get_logger(__name__)


class RAGService:
    """Orchestrates document indexing and retrieval across tfidf / vector / hybrid modes."""

    def __init__(
        self,
        mode: str = "hybrid",
        chunk_size: int = 1000,
        overlap: int = 200,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> None:
        self.mode = mode
        self._indexer = DocumentIndexer(chunk_size=chunk_size, overlap=overlap)
        self._embedding_provider = embedding_provider or get_embedding_provider()
        self._tfidf = TFIDFRetriever()
        self._vector = VectorRetriever(embedding_provider=self._embedding_provider)
        self._hybrid = HybridRetriever(embedding_provider=self._embedding_provider)
        self._chunks: list[Chunk] = []

    def index_scan_result(self, scan_result: ScanResult) -> int:
        self._chunks = self._indexer.index_scan_result(scan_result)
        self._tfidf.index(self._chunks)
        self._vector.index(self._chunks)
        self._hybrid.index(self._chunks)
        logger.info("rag_service_indexed", total_chunks=len(self._chunks), mode=self.mode)
        return len(self._chunks)

    def retrieve(self, query: str, top_k: int = 5) -> list:
        if self.mode == "tfidf":
            return self._tfidf.retrieve(query, top_k=top_k)
        if self.mode == "vector":
            results = self._vector.retrieve(query, top_k=top_k)
            return results if results else self._tfidf.retrieve(query, top_k=top_k)
        return self._hybrid.retrieve(query, top_k=top_k)

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    @property
    def embedding_available(self) -> bool:
        return self._embedding_provider.is_available
