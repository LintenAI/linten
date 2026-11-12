"""Resolve the attributes of `linten` and `linten.utils` that are imported on first access."""

import importlib
import sys
from collections.abc import Callable, Mapping
from types import MappingProxyType, ModuleType
from typing import TYPE_CHECKING, Final

from ._lazy_imports_registry import LINTEN_ATTRIBUTES, UTILS_ATTRIBUTES

if TYPE_CHECKING:
    import httpx

    from linten.linten_core_utils.tokenizer import Encoding as Tokenizer


def get_default_encoding() -> "Tokenizer":
    from linten.rust_bridge.tokenizer import get_encoding

    return get_encoding("cl100k_base")


_get_default_encoding = get_default_encoding


def _get_modified_max_tokens() -> "Callable[..., int | None]":
    from linten.linten_core_utils.token_counter import get_modified_max_tokens

    return get_modified_max_tokens


def get_token_counter_new() -> "Callable[..., int]":
    from linten.linten_core_utils.token_counter import token_counter

    return token_counter


_get_token_counter_new = get_token_counter_new


def get_messages_reach_token_count() -> "Callable[..., bool]":
    from linten.linten_core_utils.token_counter import messages_reach_token_count

    return messages_reach_token_count


_get_messages_reach_token_count = get_messages_reach_token_count


_NOT_LOADED: Final = object()


def _cached(namespace: str, name: str) -> object:
    return vars(sys.modules[namespace]).get(name, _NOT_LOADED)


def _cache(namespace: str, name: str, value: object) -> object:
    setattr(sys.modules[namespace], name, value)
    return value


def _import(namespace: str, name: str, location: tuple[str, str]) -> object:
    cached: Final = _cached(namespace, name)
    if cached is not _NOT_LOADED:
        return cached
    module_path, attr_name = location
    module: Final[ModuleType] = importlib.import_module(module_path, package="linten")
    attribute: Final[object] = getattr(module, attr_name)
    return _cache(namespace, name, attribute)


def _instance_of(class_name: str) -> Callable[[], object]:
    def create() -> object:
        cls: Final = resolve_lazy_attribute("linten", class_name)
        assert isinstance(cls, type)
        return cls()

    return create


def _submodule(module_path: str) -> Callable[[], object]:
    return lambda: importlib.import_module(module_path)


def _request_timeout() -> "float | httpx.Timeout | None":
    import httpx

    timeout: Final = _cached("linten", "request_timeout")
    return timeout if isinstance(timeout, (int, float, httpx.Timeout)) else None


def _module_level_aclient() -> object:
    from linten.llms.custom_httpx.http_handler import get_async_httpx_client

    return get_async_httpx_client(
        llm_provider="linten_module_level_client",
        params={"timeout": _request_timeout(), "client_alias": "module level aclient"},
    )


def _module_level_client() -> object:
    from linten.llms.custom_httpx.http_handler import HTTPHandler

    return HTTPHandler(timeout=_request_timeout())


def _provider_list() -> object:
    from linten.types.utils import LlmProviders

    return list(LlmProviders)


_LINTEN_FACTORIES: Final[Mapping[str, Callable[[], object]]] = MappingProxyType(
    {
        "in_memory_llm_clients_cache": _instance_of("LLMClientCache"),
        "module_level_aclient": _module_level_aclient,
        "module_level_client": _module_level_client,
        "openaiOSeriesConfig": _instance_of("OpenAIOSeriesConfig"),
        "openAIGPTConfig": _instance_of("OpenAIGPTConfig"),
        "openAIGPTAudioConfig": _instance_of("OpenAIGPTAudioConfig"),
        "openAIGPT5Config": _instance_of("OpenAIGPT5Config"),
        "nvidiaNimConfig": _instance_of("NvidiaNimConfig"),
        "nvidiaNimEmbeddingConfig": _instance_of("NvidiaNimEmbeddingConfig"),
        "priority_reservation_settings": _instance_of("PriorityReservationSettings"),
        "logging_callback_manager": _instance_of("LoggingCallbackManager"),
        "provider_list": _provider_list,
        "proxy": _submodule("linten.proxy"),
        "guardrails": _submodule("linten.guardrails"),
        "harness": _submodule("linten.harness"),
        "_service_logger": _submodule("linten._service_logger"),
    }
)


def resolve_lazy_attribute(module_name: str, name: str) -> object:
    """Import, cache and return `name`, the way `module_name.__getattr__` would."""
    linten_location: Final = LINTEN_ATTRIBUTES.get(name)
    if linten_location is not None:
        return _import("linten", name, linten_location)
    utils_location: Final = UTILS_ATTRIBUTES.get(name)
    if utils_location is not None:
        return _import("linten.utils", name, utils_location)
    factory: Final = _LINTEN_FACTORIES.get(name) if module_name == "linten" else None
    if factory is None:
        raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
    cached: Final = _cached("linten", name)
    return cached if cached is not _NOT_LOADED else _cache("linten", name, factory())
