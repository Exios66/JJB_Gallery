"""
Minimal stubs for `langchain.llms`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class OpenAI:
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"

    def __call__(self, prompt: str, **_: Any) -> str:
        raise RuntimeError(
            "This is a stub `langchain.llms.OpenAI`. Install the real `langchain` for actual execution."
        )

