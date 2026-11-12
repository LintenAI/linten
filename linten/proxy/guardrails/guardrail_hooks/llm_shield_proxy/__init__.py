from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .llm_shield_proxy import LLMShieldProxyGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail") -> LLMShieldProxyGuardrail:
    import linten

    _llm_shield_guardrail_callback: Final = LLMShieldProxyGuardrail(
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )

    linten.logging_callback_manager.add_linten_callback(_llm_shield_guardrail_callback)
    return _llm_shield_guardrail_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.LLM_SHIELD_PROXY.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.LLM_SHIELD_PROXY.value: LLMShieldProxyGuardrail,
}
