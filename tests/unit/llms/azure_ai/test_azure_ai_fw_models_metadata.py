"""
Regression tests for Azure AI Foundry Fireworks (FW-*) model cost map entries.

Prices for Data Zone pay-per-token meters come from the Azure retail prices API
(product "Azure Fireworks Models"). Kimi K3 rates come from the Microsoft Foundry
announcement. Models without dedicated Azure meters use published Fireworks
serverless rates.
"""

import json
from importlib.resources import files

import pytest


@pytest.fixture(scope="module")
def use_local_model_cost_map():
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("LINTEN_LOCAL_MODEL_COST_MAP", "True")

    import linten
    from linten.linten_core_utils.model_cost_table import publish

    original_model_cost = linten.model_cost
    linten.model_cost = json.loads(
        files("linten")
        .joinpath("model_prices_and_context_window_backup.json")
        .read_text(encoding="utf-8")
    )
    linten.get_model_info.cache_clear()
    publish(linten.model_cost)
    try:
        yield linten
    finally:
        linten.model_cost = original_model_cost
        linten.get_model_info.cache_clear()
        publish(linten.model_cost)
        monkeypatch.undo()


def test_azure_ai_fw_nemotron_lightning_supports_tool_choice(use_local_model_cost_map):
    from linten.llms.azure_ai.chat.transformation import AzureAIStudioConfig

    supported_params = AzureAIStudioConfig().get_supported_openai_params("FW-Nemotron-Lightning-3.5-30B-A3B")

    assert "tool_choice" in supported_params


def test_azure_ai_fw_kimi_k26_case_insensitive_lookup(use_local_model_cost_map):
    upper = use_local_model_cost_map.get_model_info(model="azure_ai/FW-Kimi-K2.6")
    lower = use_local_model_cost_map.get_model_info(model="azure_ai/fw-kimi-k2.6")

    assert upper["input_cost_per_token"] == pytest.approx(lower["input_cost_per_token"])
    assert upper["output_cost_per_token"] == pytest.approx(lower["output_cost_per_token"])
