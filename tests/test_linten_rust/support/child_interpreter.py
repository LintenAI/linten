from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Mapping
from typing import Final

import linten

PARENT_LINTEN_FILE: Final = "LINTEN_TEST_PARENT_LINTEN_FILE"

_PROLOGUE: Final = (
    "import os as _os, linten as _linten; _parent = _os.environ.pop({key!r}); "
    'assert _linten.__file__ == _parent, f"child imported linten from {{_linten.__file__}}, parent from {{_parent}}"; '
    "del _os, _linten, _parent\n"
)


def run_child_interpreter(
    source: str, *, env: Mapping[str, str] | None = None, timeout: float
) -> subprocess.CompletedProcess[str]:
    """Run `source` in a fresh interpreter that imports the same `linten` as this process.

    `-I` keeps the working directory off sys.path so a source checkout cannot shadow an
    installed wheel, and the prologue fails fast with both paths if the child still
    resolves a different package.
    """
    environment: Final = {**(os.environ if env is None else env), PARENT_LINTEN_FILE: linten.__file__}
    return subprocess.run(
        [sys.executable, "-I", "-c", _PROLOGUE.format(key=PARENT_LINTEN_FILE) + source],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=environment,
    )
