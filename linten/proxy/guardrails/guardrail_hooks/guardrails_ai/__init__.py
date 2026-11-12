from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .guardrails_ai import GuardrailsAI

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    if linten_params.guard_name is None:
        raise Exception(
            "GuardrailsAIException - Please pass the Guardrails AI guard name via 'linten_params::guard_name'"
        )

    _guardrails_ai_callback: Final = GuardrailsAI(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        guard_name=linten_params.guard_name,
        guardrails_ai_api_input_format=getattr(linten_params, "guardrails_ai_api_input_format", "llmOutput"),
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_guardrails_ai_callback)

    return _guardrails_ai_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.GUARDRAILS_AI.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.GUARDRAILS_AI.value: GuardrailsAI,
}
