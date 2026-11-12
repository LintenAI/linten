import importlib
import os
import subprocess
import sys
from typing import Final

import pytest

import linten
import linten.utils
from linten._lazy_imports_registry import LINTEN_ATTRIBUTES, UTILS_ATTRIBUTES
from tests.test_linten_rust.support.child_interpreter import run_child_interpreter


def test_import_linten_does_not_load_fastapi_or_bpe_table():
    result: Final = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys, linten; print(','.join(m for m in ('fastapi','starlette','linten.proxy.proxy_cli','linten.linten_core_utils.default_encoding','openai.types.realtime') if m in sys.modules))",
        ],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "LINTEN_LOCAL_MODEL_COST_MAP": "True"},
    )

    assert result.stdout.strip() == ""


def _declared(location: tuple[str, str]) -> object:
    module_path, attr_name = location
    return getattr(importlib.import_module(module_path, package="linten"), attr_name)


@pytest.mark.parametrize("name", sorted(LINTEN_ATTRIBUTES))
def test_linten_attribute_is_the_declared_object(name: str):
    assert getattr(linten, name) is _declared(LINTEN_ATTRIBUTES[name])


@pytest.mark.parametrize("name", sorted(UTILS_ATTRIBUTES))
def test_utils_attribute_is_the_same_object_from_linten_and_linten_utils(name: str):
    expected: Final = _declared(UTILS_ATTRIBUTES[name])
    assert getattr(linten.utils, name) is expected
    assert getattr(linten, name) is expected


@pytest.mark.parametrize(
    ("instance_name", "class_name"),
    [
        ("in_memory_llm_clients_cache", "LLMClientCache"),
        ("openaiOSeriesConfig", "OpenAIOSeriesConfig"),
        ("openAIGPTConfig", "OpenAIGPTConfig"),
        ("openAIGPTAudioConfig", "OpenAIGPTAudioConfig"),
        ("openAIGPT5Config", "OpenAIGPT5Config"),
        ("nvidiaNimConfig", "NvidiaNimConfig"),
        ("nvidiaNimEmbeddingConfig", "NvidiaNimEmbeddingConfig"),
        ("priority_reservation_settings", "PriorityReservationSettings"),
        ("logging_callback_manager", "LoggingCallbackManager"),
    ],
)
def test_lazy_instance_is_a_single_instance_of_its_class(instance_name: str, class_name: str):
    instance: Final = getattr(linten, instance_name)
    assert type(instance) is getattr(linten, class_name)
    assert getattr(linten, instance_name) is instance


def test_module_level_http_clients_use_request_timeout(monkeypatch: pytest.MonkeyPatch):
    client_names: Final = ("module_level_client", "module_level_aclient")
    monkeypatch.setattr(linten, "request_timeout", 7)
    for client_name in client_names:
        monkeypatch.delitem(vars(linten), client_name, raising=False)
    try:
        assert linten.module_level_client.timeout == 7
        assert linten.module_level_aclient.timeout == 7
        assert linten.module_level_client is linten.module_level_client
    finally:
        for client_name in client_names:
            vars(linten).pop(client_name, None)


def test_provider_list_lists_every_provider():
    assert linten.provider_list == list(linten.LlmProviders)


@pytest.mark.parametrize("name", ["proxy", "guardrails", "harness", "_service_logger"])
def test_submodule_attribute_is_the_submodule(name: str):
    assert getattr(linten, name) is importlib.import_module(f"linten.{name}")


@pytest.mark.parametrize("module", [linten, linten.utils])
def test_unknown_attribute_raises_attribute_error(module: object):
    with pytest.raises(AttributeError, match="not_a_linten_attribute"):
        getattr(module, "not_a_linten_attribute")
    assert not hasattr(module, "not_a_linten_attribute")


def test_linten_instances_are_not_attributes_of_linten_utils():
    assert not hasattr(linten.utils, "module_level_client")


@pytest.mark.parametrize(
    "module",
    ["linten.linten_core_utils.get_linten_params", "linten.batches.batch_utils", "linten.types.utils"],
)
def test_kwargs_funnel_and_its_importers_load_first_in_fresh_process(module: str):
    """These modules are often the first to pull in linten.types.utils, and the WIF key sets shared between
    the funnel and all_linten_params must not turn that into a cycle."""
    result = run_child_interpreter(f"import {module}", timeout=120)
    assert result.returncode == 0, result.stderr
