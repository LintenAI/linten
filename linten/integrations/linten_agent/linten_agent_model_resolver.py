"""
Hook for Linten that strips the linten_agent/ prefix from model names.

When model is linten_agent/gpt-3.5-turbo, this hook replaces it with gpt-3.5-turbo
before the completion call, similar to langfuse/model resolution.
"""

from typing import Final

from linten.integrations.custom_logger import CustomLogger
from linten.types.llms.openai import AllMessageValues
from linten.types.prompts.init_prompts import PromptSpec
from linten.types.utils import StandardCallbackDynamicParams

LINTEN_AGENT_PREFIX: Final = "linten_agent/"


class LintenAgentModelResolver(CustomLogger):
    """
    CustomLogger that strips linten_agent/ prefix from model names.

    Enables model configs like linten_agent/gpt-3.5-turbo to resolve to gpt-3.5-turbo.
    """

    def get_chat_completion_prompt(
        self,
        model: str,
        messages: list[AllMessageValues],
        non_default_params: dict,
        prompt_id: str | None,
        prompt_variables: dict | None,
        dynamic_callback_params: StandardCallbackDynamicParams,
        prompt_spec: PromptSpec | None = None,
        prompt_label: str | None = None,
        prompt_version: int | None = None,
        ignore_prompt_manager_model: bool | None = False,
        ignore_prompt_manager_optional_params: bool | None = False,
    ) -> tuple[str, list[AllMessageValues], dict]:
        """
        Strip linten_agent/ prefix from model name.

        Returns:
            (resolved_model, messages, non_default_params)
        """
        if ignore_prompt_manager_model:
            return model, messages, non_default_params
        resolved_model: Final = model.replace(LINTEN_AGENT_PREFIX, "", 1)
        return resolved_model, messages, non_default_params

    async def async_get_chat_completion_prompt(
        self,
        model: str,
        messages: list[AllMessageValues],
        non_default_params: dict,
        prompt_id: str | None,
        prompt_variables: dict | None,
        dynamic_callback_params: StandardCallbackDynamicParams,
        linten_logging_obj: object,
        prompt_spec: PromptSpec | None = None,
        tools: list[dict] | None = None,
        prompt_label: str | None = None,
        prompt_version: int | None = None,
        ignore_prompt_manager_model: bool | None = False,
        ignore_prompt_manager_optional_params: bool | None = False,
    ) -> tuple[str, list[AllMessageValues], dict]:
        """Async delegate to get_chat_completion_prompt."""
        return self.get_chat_completion_prompt(
            model=model,
            messages=messages,
            non_default_params=non_default_params,
            prompt_id=prompt_id,
            prompt_variables=prompt_variables,
            dynamic_callback_params=dynamic_callback_params,
            prompt_spec=prompt_spec,
            prompt_label=prompt_label,
            prompt_version=prompt_version,
            ignore_prompt_manager_model=ignore_prompt_manager_model,
            ignore_prompt_manager_optional_params=ignore_prompt_manager_optional_params,
        )
