"""
Test Azure AI Kimi K2.6 model metadata.
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


