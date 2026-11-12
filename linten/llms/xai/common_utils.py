from collections.abc import Iterable, Mapping
from typing import Final

import httpx
from pydantic import ConfigDict, TypeAdapter

import linten
from linten.linten_core_utils.url_utils import join_api_base
from linten.llms.base_llm.base_utils import BaseLLMModelInfo
from linten.secret_managers.main import get_secret_str
from linten.types.llms.openai import AllMessageValues
from linten.types.utils import ProviderSpecificModelInfo

USD_TICKS_PER_DOLLAR: Final = 10_000_000_000
_JSON_OBJECT: Final = TypeAdapter(Mapping[str, object], config=ConfigDict(hide_input_in_errors=True))
_JSON_VALUES: Final = TypeAdapter(Iterable[object], config=ConfigDict(hide_input_in_errors=True))
_MODEL_ID: Final = TypeAdapter(str, config=ConfigDict(strict=True, hide_input_in_errors=True))


def xai_reported_cost_in_usd(cost_in_usd_ticks: object) -> float | None:
    """xAI bills in ticks of a dollar: https://docs.x.ai/developers/cost-tracking"""
    if not isinstance(cost_in_usd_ticks, int) or isinstance(cost_in_usd_ticks, bool):
        return None
    if cost_in_usd_ticks < 0:
        return None
    return cost_in_usd_ticks / USD_TICKS_PER_DOLLAR


class XAIModelInfo(BaseLLMModelInfo):
    def get_provider_info(
        self,
        model: str,
    ) -> ProviderSpecificModelInfo | None:
        """
        Default values all models of this provider support.
        """
        return {
            "supports_web_search": True,
        }

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
        if api_key is not None:
            headers["Authorization"] = f"Bearer {api_key}"

        # Ensure Content-Type is set to application/json
        if "content-type" not in headers and "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        return headers

    @staticmethod
    def get_api_base(api_base: str | None = None) -> str | None:
        return api_base or get_secret_str("XAI_API_BASE") or "https://api.x.ai"

    @staticmethod
    def get_api_key(
        api_key: str | None = None,
        legacy_generic_before_env: bool = False,
    ) -> str | None:
        """
        Resolve xAI API keys while preserving endpoint-specific legacy order.

        Chat uses xai_key before XAI_API_KEY without adding a generic
        linten.api_key fallback. Responses and realtime historically
        preferred linten.api_key over XAI_API_KEY, so those paths opt into
        the legacy order with legacy_generic_before_env=True. In both modes,
        the provider-specific linten.xai_key takes precedence over fallbacks.
        """
        if legacy_generic_before_env:
            return api_key or linten.xai_key or linten.api_key or get_secret_str("XAI_API_KEY")

        return api_key or linten.xai_key or get_secret_str("XAI_API_KEY")

    @staticmethod
    def get_base_model(model: str) -> str | None:
        return model.replace("xai/", "")

    def get_models(self, api_key: str | None = None, api_base: str | None = None) -> list[str]:
        api_base = self.get_api_base(api_base)
        api_key = self.get_api_key(api_key)
        if api_base is None or api_key is None:
            raise ValueError(
                "XAI API base or key is not set. Set XAI_API_BASE and provide an xAI API key via api_key, linten.xai_key, or XAI_API_KEY."
            )
        response: Final = linten.module_level_client.get(
            url=join_api_base(api_base, "v1/models"),
            headers={"Authorization": f"Bearer {api_key}"},
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise Exception(
                f"Failed to fetch models from XAI. Status code: {response.status_code}, Response: {response.text}"
            )

        models: Final = _JSON_VALUES.validate_python(_JSON_OBJECT.validate_python(response.json())["data"])

        linten_model_names: Final = []
        for model in models:
            stripped_model_name = _MODEL_ID.validate_python(_JSON_OBJECT.validate_python(model)["id"])
            linten_model_name = "xai/" + stripped_model_name
            linten_model_names.append(linten_model_name)
        return linten_model_names
