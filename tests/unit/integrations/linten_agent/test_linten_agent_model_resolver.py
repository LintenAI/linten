"""Unit tests for LintenAgentModelResolver - linten_agent/ prefix model resolution."""

from unittest.mock import MagicMock

import pytest

from linten.integrations.linten_agent import LintenAgentModelResolver


class TestLintenAgentModelResolver:
    def test_get_chat_completion_prompt_strips_prefix(self):
        """Verify get_chat_completion_prompt strips linten_agent/ prefix from model."""
        resolver = LintenAgentModelResolver()
        messages = [{"role": "user", "content": "Hello"}]

        resolved_model, out_messages, out_params = resolver.get_chat_completion_prompt(
            model="linten_agent/gpt-3.5-turbo",
            messages=messages,
            non_default_params={},
            prompt_id=None,
            prompt_variables=None,
            dynamic_callback_params={},
        )

        assert resolved_model == "gpt-3.5-turbo"
        assert out_messages == messages
        assert out_params == {}

    def test_get_chat_completion_prompt_preserves_rest_of_model(self):
        """Verify model name after prefix is preserved (e.g. openai/gpt-3.5-turbo)."""
        resolver = LintenAgentModelResolver()
        messages = [{"role": "user", "content": "Test"}]

        resolved_model, _, _ = resolver.get_chat_completion_prompt(
            model="linten_agent/openai/gpt-3.5-turbo",
            messages=messages,
            non_default_params={},
            prompt_id=None,
            prompt_variables=None,
            dynamic_callback_params={},
        )

        assert resolved_model == "openai/gpt-3.5-turbo"

    def test_get_chat_completion_prompt_respects_ignore_prompt_manager_model(self):
        """Verify model is unchanged when ignore_prompt_manager_model is True."""
        resolver = LintenAgentModelResolver()
        messages = [{"role": "user", "content": "Hello"}]

        resolved_model, _, _ = resolver.get_chat_completion_prompt(
            model="linten_agent/gpt-3.5-turbo",
            messages=messages,
            non_default_params={},
            prompt_id=None,
            prompt_variables=None,
            dynamic_callback_params={},
            ignore_prompt_manager_model=True,
        )

        assert resolved_model == "linten_agent/gpt-3.5-turbo"

    @pytest.mark.asyncio
    async def test_async_get_chat_completion_prompt_strips_prefix(self):
        """Verify async_get_chat_completion_prompt strips prefix."""
        resolver = LintenAgentModelResolver()
        messages = [{"role": "user", "content": "Hello"}]

        resolved_model, out_messages, _ = (
            await resolver.async_get_chat_completion_prompt(
                model="linten_agent/gpt-3.5-turbo",
                messages=messages,
                non_default_params={},
                prompt_id=None,
                prompt_variables=None,
                dynamic_callback_params={},
                linten_logging_obj=MagicMock(),
            )
        )

        assert resolved_model == "gpt-3.5-turbo"
        assert out_messages == messages
