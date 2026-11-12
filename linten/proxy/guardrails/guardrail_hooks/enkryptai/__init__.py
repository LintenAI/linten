from .enkryptai import EnkryptAIGuardrails

__all__ = ["EnkryptAIGuardrails"]


from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _enkryptai_callback: Final = EnkryptAIGuardrails(
        guardrail_name=guardrail.get("guardrail_name", ""),
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        policy_name=linten_params.policy_name,
        deployment_name=linten_params.deployment_name,
        detectors=linten_params.detectors,
        block_on_violation=linten_params.block_on_violation,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_enkryptai_callback)

    return _enkryptai_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.ENKRYPTAI.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.ENKRYPTAI.value: EnkryptAIGuardrails,
}
