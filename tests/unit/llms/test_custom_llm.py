# What is this?
## Unit tests for the CustomLLM class


import asyncio
import importlib
import os
import time
from typing import Any, Optional, Union
from collections.abc import AsyncIterator, Callable, Iterator
from unittest.mock import AsyncMock, patch

import httpx
import openai
import pytest

import linten
from linten import (
    ChatCompletionUsageBlock,
    CustomLLM,
    GenericStreamingChunk,
    ModelResponse,
    acompletion,
    completion,
    get_llm_provider,
    image_generation,
)
from linten.linten_core_utils.logging_worker import GLOBAL_LOGGING_WORKER
from linten.llms.custom_httpx.http_handler import AsyncHTTPHandler, HTTPHandler
from linten.types.utils import (
    Delta,
    EmbeddingResponse,
    ImageObject,
    ImageResponse,
    ModelResponseStream,
    StreamingChoices,
)
from linten.utils import ModelResponseIterator
from linten.linten_core_utils.model_cost_table import publish
from tests._vcr_conftest_common import install_live_call_probe, record_vcr_outcome


class CustomModelResponseIterator:
    def __init__(self, streaming_response: Union[Iterator, AsyncIterator]):
        self.streaming_response = streaming_response

    def chunk_parser(self, chunk: Any) -> GenericStreamingChunk:
        return GenericStreamingChunk(
            text="hello world",
            tool_use=None,
            is_finished=True,
            finish_reason="stop",
            usage=ChatCompletionUsageBlock(prompt_tokens=10, completion_tokens=20, total_tokens=30),
            index=0,
        )

    # Sync iterator
    def __iter__(self):
        return self

    def __next__(self) -> GenericStreamingChunk:
        try:
            chunk: Any = self.streaming_response.__next__()  # type: ignore
        except StopIteration:
            raise StopIteration
        except ValueError as e:
            raise RuntimeError(f"Error receiving chunk from stream: {e}")

        try:
            return self.chunk_parser(chunk=chunk)
        except StopIteration:
            raise StopIteration
        except ValueError as e:
            raise RuntimeError(f"Error parsing chunk: {e},\nReceived chunk: {chunk}")

    # Async iterator
    def __aiter__(self):
        self.async_response_iterator = self.streaming_response.__aiter__()  # type: ignore
        return self.streaming_response

    async def __anext__(self) -> GenericStreamingChunk:
        try:
            chunk = await self.async_response_iterator.__anext__()
        except StopAsyncIteration:
            raise StopAsyncIteration
        except ValueError as e:
            raise RuntimeError(f"Error receiving chunk from stream: {e}")

        try:
            return self.chunk_parser(chunk=chunk)
        except StopIteration:
            raise StopIteration
        except ValueError as e:
            raise RuntimeError(f"Error parsing chunk: {e},\nReceived chunk: {chunk}")


class MyCustomLLM(CustomLLM):
    def completion(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable[..., Any],
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        linten_params=None,
        logger_fn=None,
        headers={},
        timeout: Optional[Union[float, openai.Timeout]] = None,
        client: Optional[linten.HTTPHandler] = None,
    ) -> ModelResponse:
        return linten.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello world"}],
            mock_response="Hi!",
        )  # type: ignore

    async def acompletion(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable[..., Any],
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        linten_params=None,
        logger_fn=None,
        headers={},
        timeout: Optional[Union[float, openai.Timeout]] = None,
        client: Optional[linten.AsyncHTTPHandler] = None,
    ) -> linten.ModelResponse:
        return linten.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello world"}],
            mock_response="Hi!",
        )  # type: ignore

    def streaming(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable[..., Any],
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        linten_params=None,
        logger_fn=None,
        headers={},
        timeout: Optional[Union[float, openai.Timeout]] = None,
        client: Optional[linten.HTTPHandler] = None,
    ) -> Iterator[GenericStreamingChunk]:
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": "Hello world",
            "tool_use": None,
            "usage": {"completion_tokens": 10, "prompt_tokens": 20, "total_tokens": 30},
        }

        completion_stream = ModelResponseIterator(
            model_response=generic_streaming_chunk  # type: ignore
        )
        custom_iterator = CustomModelResponseIterator(streaming_response=completion_stream)
        return custom_iterator

    async def astreaming(  # type: ignore
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable[..., Any],
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        linten_params=None,
        logger_fn=None,
        headers={},
        timeout: Optional[Union[float, openai.Timeout]] = None,
        client: Optional[linten.AsyncHTTPHandler] = None,
    ) -> AsyncIterator[GenericStreamingChunk]:  # type: ignore
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": "Hello world",
            "tool_use": None,
            "usage": {"completion_tokens": 10, "prompt_tokens": 20, "total_tokens": 30},
        }

        yield generic_streaming_chunk  # type: ignore

    def image_generation(
        self,
        model: str,
        prompt: str,
        api_key: Optional[str],
        api_base: Optional[str],
        model_response: ImageResponse,
        optional_params: dict,
        logging_obj: Any,
        timeout=None,
        client: Optional[HTTPHandler] = None,
    ):
        return ImageResponse(
            created=int(time.time()),
            data=[ImageObject(url="https://example.com/image.png")],
            response_ms=1000,
        )

    async def aimage_generation(
        self,
        model: str,
        prompt: str,
        api_key: Optional[str],
        api_base: Optional[str],
        model_response: ImageResponse,
        optional_params: dict,
        logging_obj: Any,
        timeout=None,
        client: Optional[AsyncHTTPHandler] = None,
    ):
        return ImageResponse(
            created=int(time.time()),
            data=[ImageObject(url="https://example.com/image.png")],
            response_ms=1000,
        )

    def embedding(
        self,
        model: str,
        input: list,
        model_response: EmbeddingResponse,
        print_verbose: Callable,
        logging_obj: Any,
        optional_params: dict,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        linten_params=None,
    ) -> EmbeddingResponse:
        model_response.model = model

        model_response.data = [
            {
                "object": "embedding",
                "embedding": [0.1, 0.2, 0.3],
                "index": i,
            }
            for i, _ in enumerate(input)
        ]

        return model_response

    async def aembedding(
        self,
        model: str,
        input: list,
        model_response: EmbeddingResponse,
        print_verbose: Callable,
        logging_obj: Any,
        optional_params: dict,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        linten_params=None,
    ) -> EmbeddingResponse:
        model_response.model = model

        model_response.data = [
            {
                "object": "embedding",
                "embedding": [0.1, 0.2, 0.3],
                "index": i,
            }
            for i, _ in enumerate(input)
        ]

        return model_response

    def image_edit(
        self,
        model: str,
        image: Any,
        prompt: str,
        model_response: ImageResponse,
        api_key: Optional[str],
        api_base: Optional[str],
        optional_params: dict,
        logging_obj: Any,
        timeout=None,
        client: Optional[HTTPHandler] = None,
    ) -> ImageResponse:
        return ImageResponse(
            created=int(time.time()),
            data=[ImageObject(url="https://example.com/edited-image.png")],
            response_ms=1000,
        )

    async def aimage_edit(
        self,
        model: str,
        image: Any,
        prompt: str,
        model_response: ImageResponse,
        api_key: Optional[str],
        api_base: Optional[str],
        optional_params: dict,
        logging_obj: Any,
        timeout=None,
        client: Optional[AsyncHTTPHandler] = None,
    ) -> ImageResponse:
        return ImageResponse(
            created=int(time.time()),
            data=[ImageObject(url="https://example.com/edited-image.png")],
            response_ms=1000,
        )


def test_get_llm_provider():
    """"""
    from linten.utils import custom_llm_setup

    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]

    custom_llm_setup()

    model, provider, _, _ = get_llm_provider(model="custom_llm/my-fake-model")

    assert provider == "custom_llm"


def test_simple_completion():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = completion(
        model="custom_llm/my-fake-model",
        messages=[{"role": "user", "content": "Hello world!"}],
    )

    assert resp.choices[0].message.content == "Hi!"


@pytest.mark.asyncio
async def test_simple_acompletion():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = await acompletion(
        model="custom_llm/my-fake-model",
        messages=[{"role": "user", "content": "Hello world!"}],
    )

    assert resp.choices[0].message.content == "Hi!"


def test_simple_completion_streaming():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = completion(
        model="custom_llm/my-fake-model",
        messages=[{"role": "user", "content": "Hello world!"}],
        stream=True,
    )

    for chunk in resp:
        if chunk.choices[0].finish_reason is None:
            assert isinstance(chunk.choices[0].delta.content, str)
        else:
            assert chunk.choices[0].finish_reason == "stop"


@pytest.mark.asyncio
async def test_simple_completion_async_streaming():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = await linten.acompletion(
        model="custom_llm/my-fake-model",
        messages=[{"role": "user", "content": "Hello world!"}],
        stream=True,
    )

    async for chunk in resp:
        print(chunk)
        if chunk.choices[0].finish_reason is None:
            assert isinstance(chunk.choices[0].delta.content, str)
        else:
            assert chunk.choices[0].finish_reason == "stop"


def test_simple_image_generation():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = image_generation(
        model="custom_llm/my-fake-model",
        prompt="Hello world",
    )

    print(resp)


@pytest.mark.asyncio
async def test_simple_image_generation_async():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = await linten.aimage_generation(
        model="custom_llm/my-fake-model",
        prompt="Hello world",
    )

    print(resp)


@pytest.mark.asyncio
async def test_image_generation_async_additional_params():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]

    with patch.object(my_custom_llm, "aimage_generation", new=AsyncMock()) as mock_client:
        try:
            resp = await linten.aimage_generation(
                model="custom_llm/my-fake-model",
                prompt="Hello world",
                api_key="my-api-key",
                api_base="my-api-base",
                my_custom_param="my-custom-param",
            )

            print(resp)
        except Exception as e:
            print(e)

        mock_client.assert_awaited_once()

        assert mock_client.call_args.kwargs["api_key"] == "my-api-key"
        assert mock_client.call_args.kwargs["api_base"] == "my-api-base"
        assert mock_client.call_args.kwargs["optional_params"] == {"my_custom_param": "my-custom-param"}


def test_simple_image_edit():
    """Test sync image_edit with custom handler"""
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = linten.image_edit(
        model="custom_llm/my-fake-model",
        image=b"fake_image_bytes",
        prompt="Edit this image",
    )

    print(resp)
    assert resp.data[0].url == "https://example.com/edited-image.png"


@pytest.mark.asyncio
async def test_simple_image_edit_async():
    """Test async image_edit with custom handler"""
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = await linten.aimage_edit(
        model="custom_llm/my-fake-model",
        image=b"fake_image_bytes",
        prompt="Edit this image",
    )

    print(resp)
    assert resp.data[0].url == "https://example.com/edited-image.png"


@pytest.mark.asyncio
async def test_image_edit_async_additional_params():
    """Test that additional params are passed to custom handler"""
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]

    with patch.object(
        my_custom_llm,
        "aimage_edit",
        new=AsyncMock(
            return_value=ImageResponse(
                created=int(time.time()),
                data=[ImageObject(url="https://example.com/edited-image.png")],
            )
        ),
    ) as mock_client:
        resp = await linten.aimage_edit(
            model="custom_llm/my-fake-model",
            image=b"fake_image_bytes",
            prompt="Edit this image",
            api_key="my-api-key",
            api_base="my-api-base",
            my_custom_param="my-custom-param",
        )

        print(resp)

        mock_client.assert_awaited_once()
        assert mock_client.call_args.kwargs["api_key"] == "my-api-key"
        assert mock_client.call_args.kwargs["api_base"] == "my-api-base"


def test_get_supported_openai_params():

    class MyCustomLLM(CustomLLM):
        # This is what `get_supported_openai_params` should be returning:
        def get_supported_openai_params(self, model: str) -> list[str]:
            return [
                "tools",
                "tool_choice",
                "temperature",
                "top_p",
                "top_k",
                "min_p",
                "typical_p",
                "stop",
                "seed",
                "response_format",
                "max_tokens",
                "presence_penalty",
                "frequency_penalty",
                "repeat_penalty",
                "tfs_z",
                "mirostat_mode",
                "mirostat_tau",
                "mirostat_eta",
                "logit_bias",
            ]

        def completion(self, *args, **kwargs) -> linten.ModelResponse:
            return linten.completion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello world"}],
                mock_response="Hi!",
            )  # type: ignore

    my_custom_llm = MyCustomLLM()

    linten.custom_provider_map = [  # 👈 KEY STEP - REGISTER HANDLER
        {"provider": "my-custom-llm", "custom_handler": my_custom_llm}
    ]

    resp = completion(
        model="my-custom-llm/my-fake-model",
        messages=[{"role": "user", "content": "Hello world!"}],
    )

    assert resp.choices[0].message.content == "Hi!"

    # Get supported openai params
    from linten import get_supported_openai_params

    response = get_supported_openai_params(model="my-custom-llm/my-fake-model")
    assert response is not None


def test_simple_embedding():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = linten.embedding(
        model="custom_llm/my-fake-model",
        input=["good morning from linten", "good night from linten"],
    )

    assert resp.data[1] == {
        "object": "embedding",
        "embedding": [0.1, 0.2, 0.3],
        "index": 1,
    }


@pytest.mark.asyncio
async def test_simple_aembedding():
    my_custom_llm = MyCustomLLM()
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = await linten.aembedding(
        model="custom_llm/my-fake-model",
        input=["good morning from linten", "good night from linten"],
    )

    assert resp.data[1] == {
        "object": "embedding",
        "embedding": [0.1, 0.2, 0.3],
        "index": 1,
    }


# ── Tests for ModelResponseStream passthrough in custom providers (issue #27389) ──


class ModelResponseStreamLLM(MyCustomLLM):
    """Subclass that overrides streaming/astreaming to yield ModelResponseStream directly."""

    def __init__(self, finish_reason: str = "stop"):
        self._finish_reason = finish_reason

    def streaming(self, *args, **kwargs) -> Iterator[ModelResponseStream]:  # type: ignore
        yield ModelResponseStream(
            id="test-stream-id",
            choices=[
                StreamingChoices(
                    index=0,
                    delta=Delta(content="Hello world"),
                    finish_reason=self._finish_reason,
                )
            ],
        )

    async def astreaming(self, *args, **kwargs) -> AsyncIterator[ModelResponseStream]:  # type: ignore
        yield ModelResponseStream(
            id="test-stream-id",
            choices=[
                StreamingChoices(
                    index=0,
                    delta=Delta(content="Hello world"),
                    finish_reason=self._finish_reason,
                )
            ],
        )


@pytest.mark.parametrize("finish_reason", ["stop", "tool_calls", "length", "content_filter"])
def test_custom_llm_streaming_model_response_stream(finish_reason):
    my_custom_llm = ModelResponseStreamLLM(finish_reason=finish_reason)
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = completion(
        model="custom_llm/my-fake-model",
        messages=[{"role": "user", "content": "Hello world!"}],
        stream=True,
    )

    for chunk in resp:
        print(chunk)
        if chunk.choices[0].finish_reason is None:
            assert isinstance(chunk.choices[0].delta.content, str)
        else:
            assert chunk.choices[0].finish_reason == finish_reason


@pytest.mark.asyncio
@pytest.mark.parametrize("finish_reason", ["stop", "tool_calls", "length", "content_filter"])
async def test_custom_llm_astreaming_model_response_stream(finish_reason):
    my_custom_llm = ModelResponseStreamLLM(finish_reason=finish_reason)
    linten.custom_provider_map = [{"provider": "custom_llm", "custom_handler": my_custom_llm}]
    resp = await linten.acompletion(
        model="custom_llm/my-fake-model",
        messages=[{"role": "user", "content": "Hello world!"}],
        stream=True,
    )

    async for chunk in resp:
        print(chunk)
        if chunk.choices[0].finish_reason is None:
            assert isinstance(chunk.choices[0].delta.content, str)
        else:
            assert chunk.choices[0].finish_reason == finish_reason


@pytest.fixture(autouse=True)
def _vcr_outcome_gate(request, vcr):
    install_live_call_probe(request, vcr)
    yield
    record_vcr_outcome(request, vcr)


@pytest.fixture(scope="function", autouse=True)
def isolate_linten_state():
    """
    Per-function isolation fixture.

    Resets linten globals to their true defaults before each test and
    restores them afterward, so tests don't leak side effects.
    Works safely under pytest-xdist parallel execution.
    """
    original_state = {}
    for attr in (
        "callbacks",
        "success_callback",
        "failure_callback",
        "_async_success_callback",
        "_async_failure_callback",
    ):
        if hasattr(linten, attr):
            val = getattr(linten, attr)
            original_state[attr] = val.copy() if val else []
    for attr in ("pre_call_rules", "post_call_rules"):
        if hasattr(linten, attr):
            val = getattr(linten, attr)
            original_state[attr] = val.copy() if val else []
    for attr in _SCALAR_DEFAULTS:
        if hasattr(linten, attr):
            original_state[attr] = getattr(linten, attr)
    if hasattr(linten, "in_memory_llm_clients_cache"):
        linten.in_memory_llm_clients_cache.flush_cache()
    for attr in (
        "callbacks",
        "success_callback",
        "failure_callback",
        "_async_success_callback",
        "_async_failure_callback",
        "pre_call_rules",
        "post_call_rules",
    ):
        if hasattr(linten, attr):
            setattr(linten, attr, [])
    for attr, default_val in _SCALAR_DEFAULTS.items():
        if hasattr(linten, attr):
            setattr(linten, attr, default_val)
    yield
    asyncio.run(GLOBAL_LOGGING_WORKER.clear_queue())
    if hasattr(linten, "in_memory_llm_clients_cache"):
        linten.in_memory_llm_clients_cache.flush_cache()
    for attr, original_value in original_state.items():
        if hasattr(linten, attr):
            setattr(linten, attr, original_value)
    publish(linten.model_cost)


_SCALAR_DEFAULTS = {
    "num_retries": getattr(linten, "num_retries", None),
    "num_retries_per_request": getattr(linten, "num_retries_per_request", None),
    "request_timeout": getattr(linten, "request_timeout", None),
    "set_verbose": getattr(linten, "set_verbose", False),
    "cache": getattr(linten, "cache", None),
    "allowed_fails": getattr(linten, "allowed_fails", 3),
    "default_fallbacks": getattr(linten, "default_fallbacks", None),
    "enable_azure_ad_token_refresh": getattr(linten, "enable_azure_ad_token_refresh", None),
    "tag_budget_config": getattr(linten, "tag_budget_config", None),
    "model_cost": getattr(linten, "model_cost", None),
    "token_counter": getattr(linten, "token_counter", None),
    "disable_aiohttp_transport": getattr(linten, "disable_aiohttp_transport", False),
    "force_ipv4": getattr(linten, "force_ipv4", False),
    "drop_params": getattr(linten, "drop_params", None),
    "modify_params": getattr(linten, "modify_params", False),
    "api_base": getattr(linten, "api_base", None),
    "api_key": getattr(linten, "api_key", None),
}


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """
    Module-scoped setup. Reloads linten only in single-process mode
    (skipped under xdist to avoid cross-worker interference).
    """
    import linten

    worker_id = os.environ.get("PYTEST_XDIST_WORKER", None)
    if worker_id is None:
        importlib.reload(linten)
        try:
            if hasattr(linten, "proxy") and hasattr(linten.proxy, "proxy_server"):
                import linten.proxy.proxy_server

                importlib.reload(linten.proxy.proxy_server)
        except Exception as e:
            print(f"Error reloading linten.proxy.proxy_server: {e}")
        if hasattr(linten, "in_memory_llm_clients_cache"):
            linten.in_memory_llm_clients_cache.flush_cache()
    yield
