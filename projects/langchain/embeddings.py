"""
Minimal stubs for `langchain.embeddings`.
"""

from __future__ import annotations

from typing import List, Optional


class OpenAIEmbeddings:
    def __init__(self, openai_api_key: Optional[str] = None, **_):
        self.openai_api_key = openai_api_key

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Placeholder deterministic embeddings
        return [[0.0] * 384 for _ in texts]


class HuggingFaceEmbeddings:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", **_):
        self.model_name = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[0.0] * 384 for _ in texts]

