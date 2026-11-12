from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .vigil_guard import VigilGuardGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _vigil_guard_callback: Final = VigilGuardGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        unreachable_fallback=linten_params.unreachable_fallback,
        timeout=linten_params.timeout,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )
    linten.logging_callback_manager.add_linten_callback(_vigil_guard_callback)
    return _vigil_guard_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.VIGIL_GUARD.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.VIGIL_GUARD.value: VigilGuardGuardrail,
}
