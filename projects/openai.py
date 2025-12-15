"""
Lightweight compatibility shim for the `openai` package.

Why this exists:
- Several subprojects (and their tests) patch `openai.OpenAI`.
- In minimal environments, the real `openai` dependency may not be installed.
- The stdlib `unittest.mock.patch('openai.OpenAI')` requires the module to be
  importable even if the test replaces the class.

This stub is intentionally tiny and only aims to provide the symbols that our
code/tests reference. If the real `openai` package is installed, it should be
preferred by removing this shim or adjusting PYTHONPATH accordingly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


class OpenAI:
    """
    Minimal stand-in for `openai.OpenAI`.

    The real OpenAI client is far more capable; this stub just provides the
    attribute structure used by our codepaths and unit tests.
    """

    def __init__(self, api_key: Optional[str] = None, **_: Any):
        self.api_key = api_key
        self.chat = _Chat()
        self.embeddings = _Embeddings()


class _Chat:
    def __init__(self):
        self.completions = _ChatCompletions()


class _ChatCompletions:
    def create(self, *_: Any, **__: Any) -> Any:
        raise RuntimeError(
            "This is a local stub for `openai.OpenAI`. "
            "Tests should patch this method, or install the real `openai` package."
        )


class _Embeddings:
    def create(self, *_: Any, **__: Any) -> Any:
        raise RuntimeError(
            "This is a local stub for `openai.OpenAI`. "
            "Tests should patch this method, or install the real `openai` package."
        )

