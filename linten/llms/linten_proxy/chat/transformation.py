"""
Translate from OpenAI's `/v1/chat/completions` to VLLM's `/v1/chat/completions`
"""

from typing import TYPE_CHECKING, Final

from pydantic import BaseModel, ConfigDict

import linten
from linten.constants import NON_LLM_CONNECTION_TIMEOUT, OPENAI_CHAT_COMPLETION_PARAMS
from linten.secret_managers.main import get_secret_bool, get_secret_str
from linten.types.router import Linten_Params
from linten.utils import add_path_to_api_base

from ...openai.chat.gpt_transformation import OpenAIGPTConfig

if TYPE_CHECKING:
    from linten.types.llms.openai import AllMessageValues


class _ProxyModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str


class _ProxyModelList(BaseModel):
    model_config = ConfigDict(frozen=True)

    data: tuple[_ProxyModel, ...]


class LintenProxyChatConfig(OpenAIGPTConfig):
    def get_supported_openai_params(self, model: str) -> list:
        params_list: Final = super().get_supported_openai_params(model)
        params_list.extend(OPENAI_CHAT_COMPLETION_PARAMS)
        return params_list

    def _map_openai_params(
        self,
        non_default_params: dict,
        optional_params: dict,
        model: str,
        drop_params: bool,
    ) -> dict:
        supported_openai_params: Final = self.get_supported_openai_params(model)
        for param, value in non_default_params.items():
            if param == "thinking":
                optional_params.setdefault("extra_body", {})["thinking"] = value
            elif param in supported_openai_params:
                optional_params[param] = value
        return optional_params

    def _get_openai_compatible_provider_info(
        self, api_base: str | None, api_key: str | None
    ) -> tuple[str | None, str | None]:
        api_base = api_base or get_secret_str("LINTEN_PROXY_API_BASE")
        dynamic_api_key: Final = api_key or get_secret_str("LINTEN_PROXY_API_KEY")
        return api_base, dynamic_api_key

    def get_openai_compatible_provider_info(
        self,
        api_base: str | None,
        api_key: str | None,
    ) -> tuple[str | None, str | None]:
        return self._get_openai_compatible_provider_info(api_base, api_key)

    def get_models(self, api_key: str | None = None, api_base: str | None = None) -> list[str]:
        api_base, api_key = self._get_openai_compatible_provider_info(api_base, api_key)
        if api_base is None:
            raise ValueError("api_base not set for Linten Proxy route. Set in env via `LINTEN_PROXY_API_BASE`")
        response: Final = linten.module_level_client.client.get(
            url=add_path_to_api_base(api_base, "/v1/models"),
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=NON_LLM_CONNECTION_TIMEOUT,
        )
        response.raise_for_status()
        return [f"linten_proxy/{model.id}" for model in _ProxyModelList.model_validate_json(response.content).data]

    @staticmethod
    def get_api_key(api_key: str | None = None) -> str | None:
        return api_key or get_secret_str("LINTEN_PROXY_API_KEY")

    @staticmethod
    def should_use_linten_proxy_by_default(
        linten_params: Linten_Params | None = None,
    ):
        """
        Returns True if linten proxy should be used by default for a given request

        Issue: https://github.com/LintenAI/linten/issues/10559

        Use case:
        - When using Google ADK, users want a flag to dynamically enable sending the request to linten proxy or not
        - Allow the model name to be passed in original format and still use linten proxy:
        "gemini/gemini-1.5-pro", "openai/gpt-4", "mistral/llama-2-70b-chat" etc.
        """
        import linten

        if get_secret_bool("USE_LINTEN_PROXY") is True:
            return True
        if linten_params and linten_params.use_linten_proxy is True:
            return True
        if linten.use_linten_proxy is True:
            return True
        return False

    @staticmethod
    def linten_proxy_get_custom_llm_provider_info(
        model: str, api_base: str | None = None, api_key: str | None = None
    ) -> tuple[str, str, str | None, str | None]:
        """
        Force use linten proxy for all models

        Issue: https://github.com/LintenAI/linten/issues/10559

        Expected behavior:
        - custom_llm_provider will be 'linten_proxy'
        - api_base = api_base OR LINTEN_PROXY_API_BASE
        - api_key = api_key OR LINTEN_PROXY_API_KEY

        Use case:
        - When using Google ADK, users want a flag to dynamically enable sending the request to linten proxy or not
        -  Allow the model name to be passed in original format and still use linten proxy:
        "gemini/gemini-1.5-pro", "openai/gpt-4", "mistral/llama-2-70b-chat" etc.

        Return model, custom_llm_provider, dynamic_api_key, api_base
        """
        import linten

        custom_llm_provider: Final = "linten_proxy"
        if model.startswith("linten_proxy/"):
            model = model.split("/", 1)[1]

        (
            api_base,
            api_key,
        ) = linten.LintenProxyChatConfig()._get_openai_compatible_provider_info(api_base=api_base, api_key=api_key)

        return model, custom_llm_provider, api_key, api_base

    def transform_request(
        self,
        model: str,
        messages: list["AllMessageValues"],
        optional_params: dict,
        linten_params: dict,
        headers: dict,
    ) -> dict:
        # don't transform the request
        return {
            "model": model,
            "messages": messages,
            **optional_params,
        }

    async def async_transform_request(
        self,
        model: str,
        messages: list["AllMessageValues"],
        optional_params: dict,
        linten_params: dict,
        headers: dict,
    ) -> dict:
        # don't transform the request
        return {
            "model": model,
            "messages": messages,
            **optional_params,
        }
