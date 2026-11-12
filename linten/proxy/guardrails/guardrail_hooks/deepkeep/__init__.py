from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .deepkeep import DeepKeepGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _deepkeep_guardrail_callback: Final = DeepKeepGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        firewall_id=getattr(linten_params, "deepkeep_firewall_id", None),
        unreachable_fallback=getattr(linten_params, "unreachable_fallback", "fail_closed"),
        extra_headers=getattr(linten_params, "extra_headers", None),
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )

    linten.logging_callback_manager.add_linten_callback(_deepkeep_guardrail_callback)
    return _deepkeep_guardrail_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.DEEPKEEP.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.DEEPKEEP.value: DeepKeepGuardrail,
}
