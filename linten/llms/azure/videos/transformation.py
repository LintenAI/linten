from typing import TYPE_CHECKING, Any

from linten.llms.azure.common_utils import BaseAzureLLM
from linten.llms.openai.videos.transformation import OpenAIVideoConfig
from linten.types.router import GenericLintenParams
from linten.types.videos.main import VideoCreateOptionalRequestParams

if TYPE_CHECKING:
    from linten.linten_core_utils.linten_logging import Logging as _LintenLoggingObj

    from ...base_llm.chat.transformation import BaseLLMException as _BaseLLMException
    from ...base_llm.videos.transformation import BaseVideoConfig as _BaseVideoConfig

    LintenLoggingObj = _LintenLoggingObj
    BaseVideoConfig = _BaseVideoConfig
    BaseLLMException = _BaseLLMException
else:
    LintenLoggingObj = Any
    BaseVideoConfig = Any
    BaseLLMException = Any


class AzureVideoConfig(OpenAIVideoConfig):
    """
    Configuration class for OpenAI video generation.
    """

    def __init__(self):
        super().__init__()

    def get_supported_openai_params(self, model: str) -> list:
        """
        Get the list of supported OpenAI parameters for video generation.
        """
        return [
            "model",
            "prompt",
            "input_reference",
            "seconds",
            "size",
            "user",
            "extra_headers",
        ]

    def map_openai_params(
        self,
        video_create_optional_params: VideoCreateOptionalRequestParams,
        model: str,
        drop_params: bool,
    ) -> dict:
        """No mapping applied since inputs are in OpenAI spec already"""
        return dict(video_create_optional_params)

    def validate_environment(
        self,
        headers: dict,
        model: str,
        api_key: str | None = None,
        linten_params: GenericLintenParams | None = None,
    ) -> dict:
        """
        Validate Azure environment and set up authentication headers.
        Uses _base_validate_azure_environment to properly handle credentials from linten_credential_name.
        """
        # If linten_params is provided, use it; otherwise create a new one
        if linten_params is None:
            linten_params = GenericLintenParams()

        if api_key and not linten_params.api_key:
            linten_params.api_key = api_key

        # Use the base Azure validation method which properly handles:
        # 1. Credentials from linten_credential_name via linten_params
        # 2. Sets the correct "api-key" header (not "Authorization: Bearer")
        return BaseAzureLLM.base_validate_azure_environment(headers=headers, linten_params=linten_params)

    def get_complete_url(
        self,
        model: str,
        api_base: str | None,
        linten_params: dict,
    ) -> str:
        """
        Constructs a complete URL for the API request.
        """
        return BaseAzureLLM.get_base_azure_url(
            api_base=api_base,
            linten_params=linten_params,
            route="/openai/v1/videos",
            default_api_version="",
        )
