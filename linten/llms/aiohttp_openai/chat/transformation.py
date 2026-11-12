"""
*New config* for using aiohttp to make the request to the custom OpenAI-like provider

This leads to 10x higher RPS than httpx
https://github.com/LintenAI/linten/issues/6592

New config to ensure we introduce this without causing breaking changes for users
"""

from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any, Final

from aiohttp import ClientResponse
from pydantic import ConfigDict, TypeAdapter

from linten.linten_core_utils.url_utils import ensure_api_route
from linten.llms.openai_like.chat.transformation import OpenAILikeChatConfig
from linten.types.llms.openai import AllMessageValues
from linten.types.utils import Choices, ModelResponse

if TYPE_CHECKING:
    from linten.linten_core_utils.linten_logging import Logging as _LintenLoggingObj
    from linten.linten_core_utils.tokenizer import Encoding as Tokenizer

    LintenLoggingObj = _LintenLoggingObj
else:
    LintenLoggingObj = Any

_JSON_OBJECTS: Final = TypeAdapter(
    Iterable[Mapping[str, object]], config=ConfigDict(strict=True, hide_input_in_errors=True)
)


class AiohttpOpenAIChatConfig(OpenAILikeChatConfig):
    def get_complete_url(
        self,
        api_base: str | None,
        api_key: str | None,
        model: str,
        optional_params: dict,
        linten_params: dict,
        stream: bool | None = None,
    ) -> str:
        """
        Ensure - /v1/chat/completions is at the end of the url

        """
        return ensure_api_route("https://api.openai.com" if api_base is None else api_base, "chat/completions")

    def validate_environment(
        self,
        headers: dict,
        model: str,
        messages: list[AllMessageValues],
        optional_params: dict,
        linten_params: dict,
        api_key: str | None = None,
        api_base: str | None = None,
    ) -> dict:
        return {"Authorization": f"Bearer {api_key}"}

    async def transform_response(
        self,
        model: str,
        raw_response: ClientResponse,
        model_response: ModelResponse,
        logging_obj: LintenLoggingObj,
        request_data: dict,
        messages: list[AllMessageValues],
        optional_params: dict,
        linten_params: dict,
        encoding: "Tokenizer | None",
        api_key: str | None = None,
        json_mode: bool | None = None,
    ) -> ModelResponse:
        _json_response: Final = await raw_response.json()
        model_response.id = _json_response.get("id")
        model_response.choices = [
            Choices.model_validate(choice) for choice in _JSON_OBJECTS.validate_python(_json_response.get("choices"))
        ]
        model_response.created = _json_response.get("created")
        model_response.model = _json_response.get("model")
        model_response.object = _json_response.get("object")
        model_response.system_fingerprint = _json_response.get("system_fingerprint")
        if "service_tier" in _json_response:
            return model_response.model_copy(update={"service_tier": _json_response.get("service_tier")})
        return model_response
