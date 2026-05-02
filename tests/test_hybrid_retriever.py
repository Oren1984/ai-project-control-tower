import pytest

from app.rag.chunker import chunk_text
from app.rag.embedding_provider import NullEmbeddingProvider
from app.rag.hybrid_retriever import HybridRetriever


@pytest.fixture
def sample_chunks():
    docs = [
        ("Security authentication secrets credentials management", "security.py"),
        ("Docker container deployment infrastructure CI CD", "devops.py"),
        ("Unit testing pytest coverage fixtures", "tests.py"),
    ]
    all_chunks = []
    for text, path in docs:
        all_chunks.extend(chunk_text(text, source_path=path))
    return all_chunks


def test_hybrid_falls_back_to_tfidf_without_embeddings(sample_chunks):
    retriever = HybridRetriever(embedding_provider=NullEmbeddingProvider())
    retriever.index(sample_chunks)

    results = retriever.retrieve("security secrets", top_k=2)
    assert len(results) > 0
    assert results[0].retrieval_method == "tfidf"


def test_hybrid_chunk_count(sample_chunks):
    retriever = HybridRetriever(embedding_provider=NullEmbeddingProvider())
    retriever.index(sample_chunks)
    assert retriever.chunk_count == len(sample_chunks)


def test_hybrid_empty_index():
    retriever = HybridRetriever(embedding_provider=NullEmbeddingProvider())
    retriever.index([])
    assert retriever.retrieve("test", top_k=5) == []


def test_hybrid_top_k_respected(sample_chunks):
    retriever = HybridRetriever(embedding_provider=NullEmbeddingProvider())
    retriever.index(sample_chunks)
    results = retriever.retrieve("docker testing security", top_k=1)
    assert len(results) <= 1


def test_hybrid_result_has_source_path(sample_chunks):
    retriever = HybridRetriever(embedding_provider=NullEmbeddingProvider())
    retriever.index(sample_chunks)
    results = retriever.retrieve("docker deployment", top_k=2)
    assert len(results) > 0
    for r in results:
        assert r.source_path
        assert r.text
        assert r.score >= 0.0
