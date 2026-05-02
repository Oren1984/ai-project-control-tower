import pytest

from app.rag.chunker import chunk_text


def test_single_chunk_when_text_fits():
    text = "a" * 500
    chunks = chunk_text(text, source_path="test.py", chunk_size=1000, overlap=200)
    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].chunk_index == 0
    assert chunks[0].source_path == "test.py"


def test_multiple_chunks_with_overlap():
    text = "a" * 1000 + "b" * 1000
    chunks = chunk_text(text, source_path="file.py", chunk_size=1000, overlap=200)
    assert len(chunks) >= 2
    assert chunks[1].start_char == 800  # 1000 - 200 overlap


def test_overlap_content_is_shared():
    text = "x" * 2000
    chunks = chunk_text(text, source_path="a.py", chunk_size=1000, overlap=200)
    assert len(chunks) >= 2
    overlap_in_first = chunks[0].text[800:]
    start_of_second = chunks[1].text[:200]
    assert overlap_in_first == start_of_second


def test_all_chunks_share_content_hash():
    text = "hello world " * 100
    chunks = chunk_text(text, source_path="a.py", chunk_size=500, overlap=50)
    assert len(chunks) > 1
    assert all(c.content_hash == chunks[0].content_hash for c in chunks)


def test_empty_text_returns_no_chunks():
    assert chunk_text("", source_path="empty.py") == []
    assert chunk_text("   ", source_path="whitespace.py") == []


def test_chunk_indices_are_sequential():
    text = "y" * 3000
    chunks = chunk_text(text, source_path="test.py", chunk_size=1000, overlap=100)
    for i, chunk in enumerate(chunks):
        assert chunk.chunk_index == i


def test_source_path_preserved():
    chunks = chunk_text("content", source_path="src/module.py")
    assert all(c.source_path == "src/module.py" for c in chunks)


def test_end_char_equals_len_for_last_chunk():
    text = "z" * 1500
    chunks = chunk_text(text, source_path="f.py", chunk_size=1000, overlap=200)
    assert chunks[-1].end_char == len(text)
