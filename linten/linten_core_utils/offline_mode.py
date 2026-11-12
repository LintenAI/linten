import os


def is_offline_mode() -> bool:
    """True when ``LINTEN_OFFLINE_MODE=true``. A catalog, check or tokenizer Linten fetches on its own, rather
    than from a destination the operator configured, must check this and use its bundled copy or skip instead"""
    return os.getenv("LINTEN_OFFLINE_MODE", "").strip().lower() == "true"
