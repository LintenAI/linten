from __future__ import annotations

from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .wingback import WingbackGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(
    linten_params: LintenParams,
    guardrail: Guardrail,
) -> WingbackGuardrail:
    import linten

    _wingback_callback: Final = WingbackGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        wingback_app_id=linten_params.wingback_app_id,
        additional_provider_specific_params=linten_params.additional_provider_specific_params,
        unreachable_fallback=linten_params.unreachable_fallback or "fail_closed",
        fail_on_error=linten_params.fail_on_error,
        extra_headers=linten_params.extra_headers,
        guardrail_name=guardrail["guardrail_name"],
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )

    linten.logging_callback_manager.add_linten_callback(_wingback_callback)
    return _wingback_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.WINGBACK.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.WINGBACK.value: WingbackGuardrail,
}
