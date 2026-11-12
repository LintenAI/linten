from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .noma import NomaGuardrail
from .noma_v2 import NomaV2Guardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    use_v2 = getattr(linten_params, "use_v2", False)
    if isinstance(use_v2, str):
        use_v2 = use_v2.lower() == "true"
    if use_v2:
        return initialize_guardrail_v2(linten_params=linten_params, guardrail=guardrail)

    import linten

    _noma_callback: Final = NomaGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        application_id=linten_params.application_id,
        monitor_mode=linten_params.monitor_mode,
        block_failures=linten_params.block_failures,
        anonymize_input=linten_params.anonymize_input,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_noma_callback)

    return _noma_callback


def initialize_guardrail_v2(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    extras: Final = linten_params.model_extra or {}
    _noma_v2_callback: Final = NomaV2Guardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        application_id=linten_params.application_id,
        gateway_name=linten_params.gateway_name,
        monitor_mode=linten_params.monitor_mode,
        block_failures=linten_params.block_failures,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
        streaming_buffer_until_moderated=extras.get("streaming_buffer_until_moderated"),
        streaming_end_of_stream_only=extras.get("streaming_end_of_stream_only"),
        streaming_sampling_rate=extras.get("streaming_sampling_rate"),
        streaming_buffer_release_on_scan=extras.get("streaming_buffer_release_on_scan"),
    )
    linten.logging_callback_manager.add_linten_callback(_noma_v2_callback)

    return _noma_v2_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.NOMA.value: initialize_guardrail,
    SupportedGuardrailIntegrations.NOMA_V2.value: initialize_guardrail_v2,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.NOMA.value: NomaGuardrail,
    SupportedGuardrailIntegrations.NOMA_V2.value: NomaV2Guardrail,
}
