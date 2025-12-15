"""
Minimal stubs for `langchain.text_splitter`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RecursiveCharacterTextSplitter:
    chunk_size: int = 1000
    chunk_overlap: int = 200

    def split_text(self, text: str) -> List[str]:
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap must be >= 0")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be < chunk_size")

        chunks: List[str] = []
        start = 0
        n = len(text)
        while start < n:
            end = min(start + self.chunk_size, n)
            chunks.append(text[start:end])
            if end == n:
                break
            start = end - self.chunk_overlap
        return chunks

