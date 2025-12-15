"""
Minimal stubs for `langchain.prompts`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class PromptTemplate:
    template: str
    input_variables: list[str]

    def format(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)

