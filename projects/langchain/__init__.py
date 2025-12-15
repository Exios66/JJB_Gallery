"""
Minimal `langchain` compatibility layer for this monorepo's unit tests.

Several tests import modules like:
  - `langchain.document_loaders`
  - `langchain.text_splitter`
  - `langchain.embeddings`
  - `langchain.vectorstores`
  - `langchain.chains`

Those tests also patch symbols within those modules. `unittest.mock.patch()`
requires the import targets to be importable even if the real `langchain`
dependency is not installed.

This is NOT a full LangChain implementation. It only provides the minimal API
surface required by the tests in `projects/tests/`.
"""

from __future__ import annotations

__all__ = [
    "document_loaders",
    "text_splitter",
    "embeddings",
    "vectorstores",
    "chains",
]

