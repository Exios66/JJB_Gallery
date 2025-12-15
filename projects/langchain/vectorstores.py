"""
Minimal stubs for `langchain.vectorstores`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class FAISS:
    documents: List[Any]
    embeddings: Any

    @classmethod
    def from_documents(cls, documents: List[Any], embeddings: Any) -> "FAISS":
        return cls(documents=documents, embeddings=embeddings)

    def as_retriever(self) -> Any:
        # A very small retriever stub
        class _Retriever:
            def get_relevant_documents(self, query: str) -> List[Any]:
                return []

        return _Retriever()


@dataclass
class Chroma:
    documents: List[Any]
    embeddings: Any

    @classmethod
    def from_documents(cls, documents: List[Any], embeddings: Any) -> "Chroma":
        return cls(documents=documents, embeddings=embeddings)

