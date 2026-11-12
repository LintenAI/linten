from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .xecguard import XecGuardGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(
    linten_params: "LintenParams",
    guardrail: "Guardrail",
):
    import linten

    _cb: Final = XecGuardGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        xecguard_model=linten_params.xecguard_model,
        policy_names=linten_params.policy_names,
        block_on_error=linten_params.block_on_error,
        grounding_strictness=linten_params.grounding_strictness,
        guardrail_name=guardrail.get(
            "guardrail_name",
            "",
        ),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(
        _cb,
    )

    return _cb


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.XECGUARD.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.XECGUARD.value: XecGuardGuardrail,
}
