"""
Responses API transformation for Linten Proxy provider.

Linten Proxy supports the OpenAI Responses API natively when the underlying model supports it.
This config enables pass-through behavior to the proxy's /v1/responses endpoint.
"""

from typing import Final

import httpx
from pydantic import TypeAdapter, ValidationError

from linten.linten_core_utils.url_utils import join_api_base
from linten.llms.base_llm.chat.transformation import BaseLLMException
from linten.llms.base_llm.responses.transformation import ANY_REASONING_FIELD_VALUES, ReasoningFieldValues
from linten.llms.openai.responses.transformation import OpenAIResponsesAPIConfig
from linten.secret_managers.main import get_secret_str
from linten.types.utils import LlmProviders

_ERROR_BODY: Final = TypeAdapter(dict[str, object])


def _openai_sdk_error_body(
    error_message: str,
) -> dict[str, object] | None:  # mutable-ok: BaseLLMException.body is a dict
    try:
        decoded: Final = _ERROR_BODY.validate_json(error_message)
    except ValidationError:
        return None
    nested: Final = decoded.get("error")
    return _ERROR_BODY.validate_python(nested) if isinstance(nested, dict) else decoded


class LintenProxyResponsesAPIConfig(OpenAIResponsesAPIConfig):
    """
    Configuration for Linten Proxy Responses API support.

    Extends OpenAI's config since the proxy follows OpenAI's API spec,
    but uses LINTEN_PROXY_API_BASE for the base URL.
    """

    @property
    def custom_llm_provider(self) -> LlmProviders:
        return LlmProviders.LINTEN_PROXY

    def reasoning_field_values(self) -> ReasoningFieldValues:
        return ANY_REASONING_FIELD_VALUES

    def get_complete_url(
        self,
        api_base: str | None,
        linten_params: dict,
    ) -> str:
        """
        Get the endpoint for Linten Proxy responses API.

        Uses LINTEN_PROXY_API_BASE environment variable if api_base is not provided.
        """
        api_base = api_base or get_secret_str("LINTEN_PROXY_API_BASE")

        if api_base is None:
            raise ValueError(
                "api_base not set for Linten Proxy responses API. "
                "Set via api_base parameter or LINTEN_PROXY_API_BASE environment variable"
            )

        return join_api_base(api_base, "responses")

    def get_error_class(
        self,
        error_message: str,
        status_code: int,
        headers: dict[str, object] | httpx.Headers,  # mutable-ok: inherited contract
    ) -> BaseLLMException:
        return BaseLLMException(
            status_code=status_code,
            message=error_message,
            headers=headers,
            body=_openai_sdk_error_body(error_message),
        )

    def supports_native_websocket(self) -> bool:
        """Linten Proxy does not support native WebSocket for Responses API"""
        return False
