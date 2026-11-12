from __future__ import annotations

from collections.abc import Mapping
from typing import Final

import linten
from linten.rust_bridge import failures
from linten.rust_bridge.public_call import known_params, optional_str
from linten.types.llms.openai import ResponsesAPIOptionalRequestParams, ResponsesAPIResponse

PARAMETERS: Final = tuple(ResponsesAPIOptionalRequestParams.__annotations__)


def body_params(request: Mapping[str, object]) -> Mapping[str, object]:
    return known_params(PARAMETERS, request)


def connection_defaults(provider: str) -> tuple[str | None, str | None]:
    provider_key: Final = linten.openai_key if provider == "openai" else None
    return linten.api_key or provider_key, linten.api_base


def original_previous_response_id(previous_response_id: str) -> str:
    from linten.responses.utils import ResponsesAPIRequestUtils

    return ResponsesAPIRequestUtils.decode_previous_response_id_to_original_previous_response_id(previous_response_id)


def response(value: Mapping[str, object]) -> ResponsesAPIResponse:
    return ResponsesAPIResponse.model_validate(value)


def map_failure(error: Exception, request: Mapping[str, object]) -> Exception:
    provider: Final = optional_str(request.get("custom_llm_provider")) or "openai"
    return failures.map_native_failure(
        error,
        str(request["model"]),
        provider,
        request,
        optional_str(request.get("api_base")) or optional_str(request.get("base_url")),
    )
