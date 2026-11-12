"""linten.sandbox: code-interpreter providers (see main.py) plus harness sandboxes.

`sandbox.local(path)` and `sandbox.docker(image, ...)` re-export linten.harness.sandbox.
They resolve lazily so `import linten` does not pull in linten.harness.
"""

import importlib
from typing import Final

from pydantic import TypeAdapter

_HARNESS_SANDBOX_MODULE: Final = "linten.harness.sandbox"
_HARNESS_EXPORT: Final = TypeAdapter(object)
_HARNESS_EXPORTS: Final = frozenset(
    {
        "local",
        "docker",
        "LocalSandbox",
        "DockerSandbox",
        "Sandbox",
        "Process",
        "CompletedRun",
    }
)


def __getattr__(name: str) -> object:
    if name in _HARNESS_EXPORTS:
        return _HARNESS_EXPORT.validate_python(getattr(importlib.import_module(_HARNESS_SANDBOX_MODULE), name))
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
