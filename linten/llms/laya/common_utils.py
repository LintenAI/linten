from collections.abc import Mapping
from typing import Final

from pydantic import TypeAdapter, ValidationError

from linten.types.llms.base import LintenBaseModel


class _LayaRouting(LintenBaseModel):
    model: str | None = None


def laya_response_model(response: Mapping[str, object], requested_model: str | None) -> str:
    try:
        routing: Final = TypeAdapter(_LayaRouting).validate_python(response.get("routing") or _LayaRouting())
    except ValidationError:
        return requested_model or "unknown"
    return routing.model or requested_model or "unknown"
