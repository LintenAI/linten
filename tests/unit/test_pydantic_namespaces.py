import asyncio
import importlib
import os
import warnings

import pytest

import linten
from linten.linten_core_utils.logging_worker import GLOBAL_LOGGING_WORKER
from linten.linten_core_utils.model_cost_table import publish
from tests._vcr_conftest_common import install_live_call_probe, record_vcr_outcome


def test_namespace_conflict_warning():
    with warnings.catch_warnings(record=True) as recorded_warnings:
        warnings.simplefilter("always")  # Capture all warnings
        import linten

    # Check that no warning with the specific message was raised
    assert not any("conflict with protected namespace" in str(w.message) for w in recorded_warnings), (
        "Test failed: 'conflict with protected namespace' warning was encountered!"
    )


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
        except Exception:
            pass
        if hasattr(linten, "in_memory_llm_clients_cache"):
            linten.in_memory_llm_clients_cache.flush_cache()
    yield
