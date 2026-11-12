from typing import TYPE_CHECKING, Final

from linten.types.guardrails import (
    GuardrailEventHooks,
    Mode,
    SupportedGuardrailIntegrations,
)

from .repelloai import RepelloAIGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def _event_hook_from_mode(
    mode: str | list[str] | Mode,
) -> GuardrailEventHooks | list[GuardrailEventHooks] | Mode:
    if isinstance(mode, Mode):
        return mode
    if isinstance(mode, list):
        return [GuardrailEventHooks(item) for item in mode]
    return GuardrailEventHooks(mode)


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail") -> RepelloAIGuardrail:
    import linten

    _repelloai_callback: Final = RepelloAIGuardrail(
        guardrail_name=guardrail["guardrail_name"],
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        asset_id=linten_params.asset_id,
        unreachable_fallback=linten_params.unreachable_fallback,
        event_hook=_event_hook_from_mode(linten_params.mode),
        default_on=linten_params.default_on or False,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_repelloai_callback)

    return _repelloai_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.REPELLOAI.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.REPELLOAI.value: RepelloAIGuardrail,
}
