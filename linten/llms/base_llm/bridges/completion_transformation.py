"""
Bridge for transforming API requests to another API requests
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from pydantic import BaseModel

    from linten import LintenLoggingObj, ModelResponse
    from linten.linten_core_utils.tokenizer import Encoding as Tokenizer
    from linten.llms.base_llm.base_model_iterator import BaseModelResponseIterator
    from linten.types.llms.openai import AllMessageValues


class CompletionTransformationBridge(ABC):
    @abstractmethod
    def transform_request(
        self,
        model: str,
        messages: list["AllMessageValues"],
        optional_params: dict,
        linten_params: dict,
        headers: dict,
        linten_logging_obj: "LintenLoggingObj",
    ) -> dict:
        """Transform /chat/completions api request to another request"""

    @abstractmethod
    def transform_response(
        self,
        model: str,
        raw_response: "BaseModel",  # the response from the other API
        model_response: "ModelResponse",
        logging_obj: "LintenLoggingObj",
        request_data: dict,
        messages: list["AllMessageValues"],
        optional_params: dict,
        linten_params: dict,
        encoding: "Tokenizer | None",
        api_key: str | None = None,
        json_mode: bool | None = None,
    ) -> "ModelResponse":
        """Transform another response to /chat/completions api response"""

    @abstractmethod
    def get_model_response_iterator(
        self,
        streaming_response: Union[Iterator[str], AsyncIterator[str], "ModelResponse"],
        sync_stream: bool,
        json_mode: bool | None = False,
    ) -> "BaseModelResponseIterator":
        pass
