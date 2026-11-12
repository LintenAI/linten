from typing import TYPE_CHECKING, Final

from linten.proxy.guardrails.guardrail_hooks.onyx.onyx import OnyxGuardrail
from linten.types.guardrails import SupportedGuardrailIntegrations

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _onyx_callback: Final = OnyxGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_onyx_callback)

    return _onyx_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.ONYX.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.ONYX.value: OnyxGuardrail,
}
