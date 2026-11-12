from __future__ import annotations

from typing import TYPE_CHECKING, Final

from linten.types.guardrails import (
    GuardrailEventHooks,
    Mode,
    SupportedGuardrailIntegrations,
)

from .headroom import HeadroomGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def _coerce_event_hook(
    mode: str | list[str] | Mode,
) -> GuardrailEventHooks | list[GuardrailEventHooks] | Mode:
    if isinstance(mode, Mode):
        return mode
    if isinstance(mode, list):
        return [GuardrailEventHooks(item) for item in mode]
    return GuardrailEventHooks(mode)


def initialize_guardrail(linten_params: LintenParams, guardrail: Guardrail) -> HeadroomGuardrail:
    import linten

    _callback: Final = HeadroomGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        model=linten_params.model,
        guardrail_name=guardrail["guardrail_name"],
        event_hook=_coerce_event_hook(linten_params.mode),
        default_on=linten_params.default_on or False,
        unreachable_fallback=linten_params.unreachable_fallback,
        timeout=linten_params.timeout,
        ccr_retrieval=linten_params.ccr_retrieval,
    )
    linten.logging_callback_manager.add_linten_callback(  # pyright: ignore[reportUnknownMemberType]
        _callback
    )
    return _callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.HEADROOM.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.HEADROOM.value: HeadroomGuardrail,
}
