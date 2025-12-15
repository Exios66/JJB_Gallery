"""
Minimal stubs for `langchain.chains`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RetrievalQA:
    llm: Any
    retriever: Any
    chain_type: str = "stuff"
    return_source_documents: bool = False

    @classmethod
    def from_chain_type(
        cls,
        llm: Any,
        chain_type: str,
        retriever: Any,
        return_source_documents: bool = False,
        **_: Any,
    ) -> "RetrievalQA":
        return cls(
            llm=llm,
            retriever=retriever,
            chain_type=chain_type,
            return_source_documents=return_source_documents,
        )

