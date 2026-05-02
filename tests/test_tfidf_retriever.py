import pytest

from app.rag.chunker import chunk_text
from app.rag.tfidf_retriever import TFIDFRetriever


@pytest.fixture
def sample_chunks():
    docs = [
        ("Security vulnerabilities authentication bypass secrets", "security.py"),
        ("Docker container deployment CI CD pipeline", "devops.py"),
        ("Unit testing pytest coverage assertions fixtures", "tests.py"),
        ("Architecture layers separation concerns patterns", "arch.py"),
        ("README documentation setup installation guide", "readme.md"),
    ]
    all_chunks = []
    for text, path in docs:
        all_chunks.extend(chunk_text(text, source_path=path))
    return all_chunks


def test_index_and_retrieve(sample_chunks):
    retriever = TFIDFRetriever()
    retriever.index(sample_chunks)

    assert retriever.is_fitted
    assert retriever.chunk_count == len(sample_chunks)


def test_relevant_result_returned(sample_chunks):
    retriever = TFIDFRetriever()
    retriever.index(sample_chunks)

    results = retriever.retrieve("security authentication", top_k=3)
    assert len(results) > 0
    assert results[0].source_path == "security.py"
    assert results[0].score > 0.0


def test_empty_index_returns_empty():
    retriever = TFIDFRetriever()
    assert retriever.retrieve("anything", top_k=5) == []


def test_no_match_returns_empty(sample_chunks):
    retriever = TFIDFRetriever()
    retriever.index(sample_chunks)
    results = retriever.retrieve("zzzzxxxxxqqqqqwwww", top_k=5)
    assert results == []


def test_top_k_is_respected(sample_chunks):
    retriever = TFIDFRetriever()
    retriever.index(sample_chunks)
    results = retriever.retrieve("docker testing security documentation", top_k=2)
    assert len(results) <= 2


def test_result_fields_present(sample_chunks):
    retriever = TFIDFRetriever()
    retriever.index(sample_chunks)
    results = retriever.retrieve("testing pytest", top_k=1)
    assert len(results) == 1
    r = results[0]
    assert r.chunk_index >= 0
    assert r.source_path
    assert r.text
    assert r.score > 0.0
    assert r.content_hash
    assert r.retrieval_method == "tfidf"


def test_index_empty_chunks():
    retriever = TFIDFRetriever()
    retriever.index([])
    assert not retriever.is_fitted
    assert retriever.chunk_count == 0
