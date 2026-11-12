from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .qohash import QostodianNexus

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _instance: Final = QostodianNexus(
        api_base=linten_params.api_base,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        additional_provider_specific_params=linten_params.additional_provider_specific_params,
        extra_headers=getattr(linten_params, "extra_headers", None),
        timeout=linten_params.timeout,
    )

    linten.logging_callback_manager.add_linten_callback(_instance)

    return _instance


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.QOSTODIAN_NEXUS.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.QOSTODIAN_NEXUS.value: QostodianNexus,
}
