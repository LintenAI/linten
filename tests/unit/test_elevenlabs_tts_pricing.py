"""ElevenLabs text-to-speech prices match the published API rates.

https://elevenlabs.io/pricing/api lists "v3" and "v2 Multilingual" at $0.08 and
"Flash / Turbo" at $0.04, each "Price per 1K characters", and says API usage is
billed in US dollars, not credits. The map had v3 and Multilingual v2 at a
Scale-plan credit estimate ($0.18 per 1K characters) and no Flash rows.
"""

import json
from pathlib import Path

import pytest

import linten

REPO_ROOT = Path(__file__).parents[2]
PRICES = {
    "elevenlabs/eleven_v3": 8e-05,
    "elevenlabs/eleven_multilingual_v2": 8e-05,
    "elevenlabs/eleven_flash_v2_5": 4e-05,
    "elevenlabs/eleven_flash_v2": 4e-05,
}


@pytest.fixture(autouse=True)
def local_model_cost_map(monkeypatch):
    """Never depend on the published cost map having these rows yet."""
    monkeypatch.setenv("LINTEN_LOCAL_MODEL_COST_MAP", "True")
    monkeypatch.setattr(linten, "model_cost", linten.get_model_cost_map(url=""))
    linten.get_model_info.cache_clear()
    yield
    linten.get_model_info.cache_clear()


@pytest.mark.parametrize("model, per_character", PRICES.items())
def test_metadata_and_backup(model, per_character):
    main = json.loads((REPO_ROOT / "model_prices_and_context_window.json").read_text())
    backup = json.loads((REPO_ROOT / "linten/model_prices_and_context_window_backup.json").read_text())
    assert main[model] == backup[model]
    info = linten.get_model_info(model)
    assert info["linten_provider"] == "elevenlabs"
    assert info["mode"] == "audio_speech"
    assert info["input_cost_per_character"] == per_character


@pytest.mark.parametrize("model, per_character", PRICES.items())
def test_speech_cost_is_charged_per_character(model, per_character):
    cost = linten.completion_cost(model=model, call_type="speech", prompt="x" * 1000)
    assert cost == pytest.approx(per_character * 1000)
