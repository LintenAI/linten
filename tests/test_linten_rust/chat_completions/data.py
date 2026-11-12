from typing import Final

import linten
from tests.test_linten_rust.messages.data import MESSAGES, MESSAGES_MODEL
from tests.test_linten_rust.support.recording_server import RecordingServer
from tests.test_linten_rust.support.routing import call_public


def _error(kind: str) -> dict[str, object]:
    return {"type": "error", "error": {"type": kind, "message": kind}}


REQUEST: Final = {"model": MESSAGES_MODEL, "messages": list(MESSAGES), "max_tokens": 32}
BAD_REQUEST: Final = _error("invalid_request_error")
RATE_LIMITED: Final = _error("rate_limit_error")


async def call(server: RecordingServer, *, asynchronous: bool = True, **kwargs: object) -> object:
    return await call_public(
        linten.completion,
        linten.acompletion,
        REQUEST,
        server,
        asynchronous=asynchronous,
        **kwargs,
    )
