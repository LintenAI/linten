import re
from collections.abc import Callable, Collection, Mapping, Sequence
from types import MappingProxyType
from typing import TYPE_CHECKING, Final, Optional

import httpx
from httpx import Response

from linten.linten_core_utils.linten_logging import Logging
from linten.llms.azure.common_utils import BaseAzureLLM
from linten.llms.base_llm.passthrough.transformation import (
    BasePassthroughConfig,
    replace_path_segment,
    strip_leading_model_segment,
)
from linten.llms.openai_like.passthrough.transformation import logged_openai_like_response, logged_openai_like_stream
from linten.secret_managers.main import get_secret_str
from linten.types.llms.openai import AllMessageValues
from linten.types.router import GenericLintenParams

if TYPE_CHECKING:
    from httpx import URL

    from linten.llms.base_llm.passthrough.transformation import LoggedRelayResponse


AZURE_DEPLOYMENT_SEGMENT: Final = re.compile(r"(?<![^/])openai/deployments/([^/]+)")
AZURE_BODY_MODEL_INFERENCE_ENDPOINTS: Final = frozenset(
    {"responses", "chat/completions", "completions", "embeddings", "images/generations", "audio/speech"}
)


def is_azure_body_model_inference_endpoint(endpoint: str) -> bool:
    if AZURE_DEPLOYMENT_SEGMENT.search(endpoint) is not None:
        return False
    path: Final = endpoint.strip("/")
    return any(path == name or path.endswith(f"/{name}") for name in AZURE_BODY_MODEL_INFERENCE_ENDPOINTS)


def azure_router_model_in_endpoint(endpoint: str, router_models: Collection[str]) -> str | None:
    parts: Final = endpoint.split("/")
    if len(parts) < 2:
        return None
    return next((part for part in parts if part in router_models), None)


def foreign_azure_deployment(
    endpoint: str, model_group: str, served_models: Callable[[], Collection[str]]
) -> str | None:
    match: Final = AZURE_DEPLOYMENT_SEGMENT.search(endpoint)
    if match is None:
        return None
    deployment: Final = match.group(1)
    if deployment == model_group:
        return None
    served: Final = frozenset(name.casefold() for name in served_models())
    return None if deployment.casefold() in served else deployment


def without_api_version(api_base: str) -> str:
    url: Final = httpx.URL(api_base)
    kept_params: Final = tuple((key, value) for key, value in url.params.multi_items() if key != "api-version")
    return str(url.copy_with(params=httpx.QueryParams(kept_params)))


class AzurePassthroughConfig(BasePassthroughConfig):
    def is_streaming_request(self, endpoint: str, request_data: dict) -> bool:
        return bool(request_data.get("stream"))

    def get_complete_url(
        self,
        api_base: str | None,
        api_key: str | None,
        model: str,
        endpoint: str,
        request_query_params: dict | None,
        linten_params: dict,
    ) -> tuple["URL", str]:
        base_target_url: Final = self.get_api_base(api_base)

        if base_target_url is None:
            raise Exception("Azure api base not found")

        linten_metadata: Final = linten_params.get("linten_metadata") or {}
        model_group: Final = linten_metadata.get("model_group")
        routed_endpoint: Final = replace_path_segment(endpoint, model_group, model) if model_group else endpoint
        native_endpoint: Final = strip_leading_model_segment(routed_endpoint, (model,))

        caller_api_version: Final = request_query_params.get("api-version") if request_query_params else None
        relay_base: Final = without_api_version(base_target_url) if caller_api_version else base_target_url
        complete_url: Final = BaseAzureLLM.get_base_azure_url(
            api_base=relay_base,
            linten_params=MappingProxyType(
                {**linten_params, "api_version": caller_api_version or linten_params.get("api_version")}
            ),
            route=native_endpoint,
        )
        return (
            httpx.URL(complete_url),
            base_target_url,
        )

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
        return BaseAzureLLM.base_validate_azure_environment(
            headers=headers,
            linten_params=GenericLintenParams.model_validate({**linten_params, "api_key": api_key}),
        )

    @staticmethod
    def get_api_base(
        api_base: str | None = None,
    ) -> str | None:
        return api_base or get_secret_str("AZURE_API_BASE")

    @staticmethod
    def get_api_key(
        api_key: str | None = None,
    ) -> str | None:
        return api_key or get_secret_str("AZURE_API_KEY")

    @staticmethod
    def get_base_model(model: str) -> str | None:
        return model

    def get_models(self, api_key: str | None = None, api_base: str | None = None) -> list[str]:
        return super().get_models(api_key, api_base)

    def logging_non_streaming_response(
        self,
        model: str,
        custom_llm_provider: str,
        httpx_response: Response,
        request_data: Mapping[str, object],
        logging_obj: Logging,
        endpoint: str,
    ) -> Optional["LoggedRelayResponse"]:
        return logged_openai_like_response(model, httpx_response, request_data, logging_obj, endpoint)

    def handle_logging_collected_chunks(
        self,
        all_chunks: Sequence[str],
        linten_logging_obj: Logging,
        model: str,
        custom_llm_provider: str,
        endpoint: str,
    ) -> Optional["LoggedRelayResponse"]:
        return logged_openai_like_stream(all_chunks, linten_logging_obj, model, endpoint)
