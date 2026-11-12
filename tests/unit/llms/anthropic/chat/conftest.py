"""Force ``linten.model_cost`` to load from the PR-local JSON for these tests.

By default ``linten.model_cost`` is fetched from the main branch on GitHub,
which lags behind PR-branch flag additions. This fixture loads the local
file so per-model flag tests pass in CI as well as locally.
See https://github.com/LintenAI/linten/issues/27122.
"""

import pytest

import linten
from linten.linten_core_utils.get_model_cost_map import get_model_cost_map


@pytest.fixture(autouse=True)
def _use_pr_local_model_cost_map(monkeypatch):
    monkeypatch.setenv("LINTEN_LOCAL_MODEL_COST_MAP", "True")
    monkeypatch.setattr(
        linten,
        "model_cost",
        get_model_cost_map(url=linten.model_cost_map_url),
    )
    yield
