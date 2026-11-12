from typing import TYPE_CHECKING, Final

from linten.proxy.guardrails.guardrail_hooks.airia.airia import AiriaGuardrail
from linten.types.guardrails import SupportedGuardrailIntegrations

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail") -> AiriaGuardrail:
    import linten

    _airia_callback: Final = AiriaGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        timeout=linten_params.timeout,
        guardrail_name=guardrail["guardrail_name"],
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )
    linten.logging_callback_manager.add_linten_callback(_airia_callback)

    return _airia_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.AIRIA.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.AIRIA.value: AiriaGuardrail,
}
