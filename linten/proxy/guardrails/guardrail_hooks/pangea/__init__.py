from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .pangea import PangeaHandler

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    guardrail_name: Final = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Pangea guardrail name is required")

    _pangea_callback: Final = PangeaHandler(
        guardrail_name=guardrail_name,
        pangea_input_recipe=linten_params.pangea_input_recipe,
        pangea_output_recipe=linten_params.pangea_output_recipe,
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_pangea_callback)

    return _pangea_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.PANGEA.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.PANGEA.value: PangeaHandler,
}
