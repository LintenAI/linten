from typing import TYPE_CHECKING, Any, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .generic_guardrail_api import GenericGuardrailAPI

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def _get_config_value(linten_params: "LintenParams", optional_params: object, attribute_name: str) -> Any | None:
    if optional_params is not None:
        value: Final = (
            optional_params.get(attribute_name)
            if isinstance(optional_params, dict)
            else getattr(optional_params, attribute_name, None)
        )
        if value is not None:
            return value
    return getattr(linten_params, attribute_name, None)


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    optional_params: Final = getattr(linten_params, "optional_params", None)

    _generic_guardrail_api_callback: Final = GenericGuardrailAPI(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        headers=getattr(linten_params, "headers", None),
        additional_provider_specific_params=getattr(linten_params, "additional_provider_specific_params", {}),
        unreachable_fallback=getattr(linten_params, "unreachable_fallback", "fail_closed"),
        fail_on_error=getattr(linten_params, "fail_on_error", True),
        forward_messages_as_sent=linten_params.forward_messages_as_sent,
        extra_headers=getattr(linten_params, "extra_headers", None),
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        streaming_end_of_stream_only=_get_config_value(linten_params, optional_params, "streaming_end_of_stream_only"),
        streaming_sampling_rate=_get_config_value(linten_params, optional_params, "streaming_sampling_rate"),
        streaming_transform_mode=_get_config_value(linten_params, optional_params, "streaming_transform_mode"),
        streaming_buffer_until_moderated=_get_config_value(
            linten_params, optional_params, "streaming_buffer_until_moderated"
        ),
        timeout=linten_params.timeout,
        num_retries=linten_params.num_retries,
    )

    linten.logging_callback_manager.add_linten_callback(_generic_guardrail_api_callback)
    return _generic_guardrail_api_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.GENERIC_GUARDRAIL_API.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.GENERIC_GUARDRAIL_API.value: GenericGuardrailAPI,
}
