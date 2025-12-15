"""
Minimal stubs for `langchain.document_loaders`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Document:
    page_content: str


class TextLoader:
    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> List[Document]:
        text = Path(self.file_path).read_text(encoding=self.encoding)
        return [Document(page_content=text)]


class PyPDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        # PDF parsing is intentionally not implemented in this stub.
        raise NotImplementedError(
            "PyPDFLoader is a stub. Install the real `langchain`/PDF dependencies "
            "to enable PDF loading."
        )


class DirectoryLoader:
    def __init__(self, path: str, glob: str = "**/*"):
        self.path = path
        self.glob = glob

    def load(self) -> List[Document]:
        # Directory walking is intentionally not implemented in this stub.
        raise NotImplementedError(
            "DirectoryLoader is a stub. Install the real `langchain` to enable directory loading."
        )

