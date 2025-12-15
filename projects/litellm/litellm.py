"""
Minimal `litellm` shim colocated with the LiteLLM proxy example.

The unit tests add `projects/litellm/` directly to `sys.path` and then patch
`litellm.completion`. Without a `litellm.py` module in that directory, Python
may resolve `import litellm` to an unrelated namespace package, and the patch
fails because `completion` is missing.

This shim provides `completion` and `acompletion` so:
- tests can patch them reliably
- `proxy_server.py` can import them in minimal environments
"""

from __future__ import annotations

from typing import Any


def completion(*_: Any, **__: Any) -> Any:
    raise RuntimeError(
        "This is a local `litellm` shim. Tests should patch `litellm.completion`, "
        "or install the real `litellm` dependency."
    )


async def acompletion(*_: Any, **__: Any) -> Any:
    raise RuntimeError(
        "This is a local `litellm` shim. Tests should patch `litellm.acompletion`, "
        "or install the real `litellm` dependency."
    )

