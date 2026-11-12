"""Rubrik guardrail integration for Linten."""

from typing import TYPE_CHECKING, Final

from linten.integrations.rubrik import RubrikLogger
from linten.types.guardrails import SupportedGuardrailIntegrations

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail") -> RubrikLogger:
    """Create and register a RubrikLogger instance.

    The ``mode`` field in the guardrail config controls which surfaces are
    moderated:
    - ``pre_call`` (or a mode that includes it): prompt moderation via the
      ``/v1/before_prompt/openai/v1`` webhook.
    - ``post_call`` (the default when ``mode`` is omitted): response and tool
      call moderation via the ``/v1/after_completion/openai/v1`` webhook.

    Both hooks are active when ``mode`` covers both ``pre_call`` and
    ``post_call``.
    """
    import linten

    rubrik_callback: Final = RubrikLogger(
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )

    linten.logging_callback_manager.add_linten_callback(rubrik_callback)
    return rubrik_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.RUBRIK.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.RUBRIK.value: RubrikLogger,
}
