from typing import Final

import importlib_metadata


def _installed_version(distribution: str) -> str | None:
    try:
        return importlib_metadata.version(distribution)
    except Exception:
        return None


_legacy_version: Final = _installed_version("linten")
_core_version: Final = _installed_version("linten-core")

if _legacy_version is not None and _core_version is not None:
    raise RuntimeError(
        "linten and linten-core are both installed and share the linten namespace. "
        "Install them in separate environments."
    )

version = _legacy_version or _core_version or "unknown"
