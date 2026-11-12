import asyncio
import importlib

import pytest

import linten
from linten import get_llm_provider
from tests._vcr_conftest_common import install_live_call_probe, record_vcr_outcome


def test_get_llm_provider_hyperbolic():
    """Test that hyperbolic/ prefix returns the correct provider"""
    model, provider, _, _ = get_llm_provider(model="hyperbolic/deepseek-v3")
    assert provider == "hyperbolic"
    assert model == "deepseek-v3"


def test_hyperbolic_completion_call():
    """Test basic completion call structure for Hyperbolic"""
    # This is primarily a structure test since we don't have actual API keys
    linten.set_verbose = True
    response = linten.completion(
        model="hyperbolic/qwen-2.5-72b",
        messages=[{"role": "user", "content": "Hello!"}],
        mock_response="Hi there!",
    )
    assert response is not None


def test_hyperbolic_config_initialization():
    """Test that HyperbolicChatConfig initializes correctly"""
    from linten.llms.hyperbolic.chat.transformation import HyperbolicChatConfig

    config = HyperbolicChatConfig()
    assert config.custom_llm_provider == "hyperbolic"


def test_hyperbolic_get_openai_compatible_provider_info():
    """Test API base and key handling"""
    from linten.llms.hyperbolic.chat.transformation import HyperbolicChatConfig

    config = HyperbolicChatConfig()

    # Test default API base
    api_base, api_key = config.get_openai_compatible_provider_info(None, None)
    assert api_base == "https://api.hyperbolic.xyz/v1"
    # api_key may be set from environment, so we don't test for None

    # Test custom API base
    custom_base = "https://custom.hyperbolic.com/v1"
    api_base, api_key = config.get_openai_compatible_provider_info(custom_base, "test-key")
    assert api_base == custom_base
    assert api_key == "test-key"


def test_hyperbolic_in_provider_lists():
    """Test that hyperbolic is in all relevant provider lists"""
    from linten.constants import (
        openai_compatible_endpoints,
        openai_compatible_providers,
        openai_text_completion_compatible_providers,
    )

    assert "hyperbolic" in openai_compatible_providers
    assert "hyperbolic" in openai_text_completion_compatible_providers
    assert "https://api.hyperbolic.xyz/v1" in openai_compatible_endpoints


def test_hyperbolic_supported_params():
    """Test that supported OpenAI parameters are correctly configured"""
    from linten.llms.hyperbolic.chat.transformation import HyperbolicChatConfig

    config = HyperbolicChatConfig()
    supported_params = config.get_supported_openai_params("hyperbolic/deepseek-v3")

    # Check for essential parameters
    assert "messages" in supported_params
    assert "model" in supported_params
    assert "stream" in supported_params
    assert "temperature" in supported_params
    assert "max_tokens" in supported_params
    assert "tools" in supported_params
    assert "tool_choice" in supported_params


@pytest.fixture(autouse=True)
def _vcr_outcome_gate(request, vcr):
    install_live_call_probe(request, vcr)
    yield
    record_vcr_outcome(request, vcr)


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown(event_loop):
    import linten

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
    for attr in _SCALAR_DEFAULTS:
        if hasattr(linten, attr):
            original_state[attr] = getattr(linten, attr)
    from linten.linten_core_utils.logging_worker import GLOBAL_LOGGING_WORKER

    asyncio.run(GLOBAL_LOGGING_WORKER.clear_queue())
    importlib.reload(linten)
    asyncio.set_event_loop(event_loop)
    yield
    for attr, original_value in original_state.items():
        if hasattr(linten, attr):
            setattr(linten, attr, original_value)
    pending = asyncio.all_tasks(event_loop)
    for task in pending:
        task.cancel()
    if pending:
        event_loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))


_SCALAR_DEFAULTS = {
    "num_retries": getattr(linten, "num_retries", None),
    "set_verbose": getattr(linten, "set_verbose", False),
    "cache": getattr(linten, "cache", None),
    "allowed_fails": getattr(linten, "allowed_fails", 3),
    "disable_aiohttp_transport": getattr(linten, "disable_aiohttp_transport", False),
    "force_ipv4": getattr(linten, "force_ipv4", False),
    "drop_params": getattr(linten, "drop_params", None),
    "modify_params": getattr(linten, "modify_params", False),
    "api_base": getattr(linten, "api_base", None),
    "api_key": getattr(linten, "api_key", None),
    "cohere_key": getattr(linten, "cohere_key", None),
}
