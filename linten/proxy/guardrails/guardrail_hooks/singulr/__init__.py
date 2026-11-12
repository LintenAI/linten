from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .singulr import SingulrGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(
    linten_params: "LintenParams",
    guardrail: "Guardrail",
):
    import linten

    _cb: Final = SingulrGuardrail(
        singulr_api_base=getattr(linten_params, "singulr_api_base", None) or linten_params.api_base,
        singulr_api_key=getattr(linten_params, "singulr_api_key", None) or linten_params.api_key,
        singulr_application_id=getattr(linten_params, "singulr_application_id", None),
        singulr_guardrail_id=getattr(linten_params, "singulr_guardrail_id", None),
        block_on_error=getattr(linten_params, "block_on_error", None),
        timeout=linten_params.timeout,
        guardrail_name=guardrail.get(
            "guardrail_name",
            "",
        ),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )
    linten.logging_callback_manager.add_linten_callback(
        _cb,
    )

    return _cb


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.SINGULR.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.SINGULR.value: SingulrGuardrail,
}
