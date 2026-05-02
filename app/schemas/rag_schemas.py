from __future__ import annotations

from pydantic import BaseModel


class ChunkSchema(BaseModel):
    text: str
    source_path: str
    content_hash: str
    chunk_index: int
    start_char: int
    end_char: int


class RetrievalResultSchema(BaseModel):
    chunk_index: int
    source_path: str
    text: str
    score: float
    content_hash: str
    retrieval_method: str


class RAGContextSchema(BaseModel):
    query: str
    results: list[RetrievalResultSchema]
    total_chunks_indexed: int
    retrieval_method: str
