from __future__ import annotations

import httpx

from linten.rust_bridge import public_call


def timeout_to_seconds(timeout: float | httpx.Timeout | None) -> float | None:
    return public_call.timeout_to_seconds(timeout)
