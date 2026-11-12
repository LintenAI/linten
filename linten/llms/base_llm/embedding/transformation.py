from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import httpx

from linten.llms.base_llm.chat.transformation import BaseConfig
from linten.types.llms.openai import AllEmbeddingInputValues, AllMessageValues
from linten.types.utils import EmbeddingResponse, ModelResponse

if TYPE_CHECKING:
    from linten.linten_core_utils.linten_logging import Logging as _LintenLoggingObj
    from linten.linten_core_utils.tokenizer import Encoding as Tokenizer

    LintenLoggingObj = _LintenLoggingObj
else:
    LintenLoggingObj = Any


class BaseEmbeddingConfig(BaseConfig, ABC):
    @abstractmethod
    def transform_embedding_request(
        self,
        model: str,
        input: AllEmbeddingInputValues,
        optional_params: dict,
        headers: dict,
    ) -> dict:
        return {}

    @abstractmethod
    def transform_embedding_response(
        self,
        model: str,
        raw_response: httpx.Response,
        model_response: EmbeddingResponse,
        logging_obj: LintenLoggingObj,
        api_key: str | None,
        request_data: dict,
        optional_params: dict,
        linten_params: dict,
    ) -> EmbeddingResponse:
        return model_response

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
        OPTIONAL

        Get the complete url for the request

        Some providers need `model` in `api_base`
        """
        return api_base or ""

    def transform_request(
        self,
        model: str,
        messages: list[AllMessageValues],
        optional_params: dict,
        linten_params: dict,
        headers: dict,
    ) -> dict:
        raise NotImplementedError("EmbeddingConfig does not need a request transformation for chat models")

    def transform_response(
        self,
        model: str,
        raw_response: httpx.Response,
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
        raise NotImplementedError("EmbeddingConfig does not need a response transformation for chat models")
