"""
Lightweight compatibility shim for the `streamlit` package.

Some unit tests patch `streamlit.set_page_config` and `streamlit.markdown`.
`unittest.mock.patch()` requires the module to be importable even if Streamlit
is not installed. This stub provides the minimal surface area needed.
"""

from __future__ import annotations

from typing import Any, Optional


def set_page_config(*_: Any, **__: Any) -> None:
    return None


def markdown(*_: Any, **__: Any) -> None:
    return None


def error(*_: Any, **__: Any) -> None:
    return None


def warning(*_: Any, **__: Any) -> None:
    return None


def info(*_: Any, **__: Any) -> None:
    return None


def success(*_: Any, **__: Any) -> None:
    return None


def write(*_: Any, **__: Any) -> None:
    return None


def title(*_: Any, **__: Any) -> None:
    return None


class _SessionState(dict):
    pass


session_state = _SessionState()

