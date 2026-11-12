from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .akto import AktoGuardrail, streaming_sampling_rate_from

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _akto_callback: Final = AktoGuardrail(
        akto_base_url=linten_params.akto_base_url,
        akto_api_key=linten_params.akto_api_key,
        akto_account_id=linten_params.akto_account_id,
        akto_vxlan_id=linten_params.akto_vxlan_id,
        context_source=linten_params.context_source,
        akto_metadata=linten_params.akto_metadata,
        streaming_sampling_rate=streaming_sampling_rate_from(linten_params),
        guardrail_timeout=linten_params.guardrail_timeout,
        file_guardrail_timeout=linten_params.file_guardrail_timeout,
        unreachable_fallback=linten_params.unreachable_fallback,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )

    linten.logging_callback_manager.add_linten_callback(_akto_callback)
    return _akto_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.AKTO.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.AKTO.value: AktoGuardrail,
}
