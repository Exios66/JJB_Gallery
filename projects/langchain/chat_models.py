"""
Minimal stubs for `langchain.chat_models`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ChatOpenAI:
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"

    def invoke(self, *_: Any, **__: Any) -> Any:
        raise RuntimeError(
            "This is a stub `langchain.chat_models.ChatOpenAI`. Install the real `langchain` for actual execution."
        )

