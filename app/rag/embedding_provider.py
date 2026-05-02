from __future__ import annotations

from abc import ABC, abstractmethod

EMBEDDING_DIM = 384


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        ...

    @property
    @abstractmethod
    def is_available(self) -> bool:
        ...


class NullEmbeddingProvider(EmbeddingProvider):
    """Returns zero vectors. System runs fully without ML dependencies."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * EMBEDDING_DIM for _ in texts]

    @property
    def dimension(self) -> int:
        return EMBEDDING_DIM

    @property
    def is_available(self) -> bool:
        return False


class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model_name = model_name
        self._model = None
        self._available = False
        self._dim = EMBEDDING_DIM
        self._try_load()

    def _try_load(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore

            self._model = SentenceTransformer(self._model_name)
            self._dim = self._model.get_sentence_embedding_dimension()
            self._available = True
        except (ImportError, Exception):
            pass

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not self._available or self._model is None:
            return [[0.0] * self._dim for _ in texts]
        return self._model.encode(texts, show_progress_bar=False).tolist()

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def is_available(self) -> bool:
        return self._available


def get_embedding_provider() -> EmbeddingProvider:
    provider = SentenceTransformerProvider()
    if provider.is_available:
        return provider
    return NullEmbeddingProvider()
