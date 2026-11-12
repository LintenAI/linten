"""Gray Swan Cygnal guardrail integration for Linten."""

from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .grayswan import (
    GraySwanGuardrail,
    GraySwanGuardrailAPIError,
    GraySwanGuardrailMissingSecrets,
)

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail") -> GraySwanGuardrail:
    import linten

    guardrail_name: Final = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Gray Swan guardrail requires a guardrail_name")

    optional_params: Final = getattr(linten_params, "optional_params", None)

    grayswan_guardrail: Final = GraySwanGuardrail(
        guardrail_name=guardrail_name,
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        on_flagged_action=_get_config_value(linten_params, optional_params, "on_flagged_action"),
        violation_threshold=_get_config_value(linten_params, optional_params, "violation_threshold"),
        reasoning_mode=_get_config_value(linten_params, optional_params, "reasoning_mode"),
        categories=_get_config_value(linten_params, optional_params, "categories"),
        policy_id=_get_config_value(linten_params, optional_params, "policy_id"),
        streaming_end_of_stream_only=_get_config_value(linten_params, optional_params, "streaming_end_of_stream_only")
        or False,
        streaming_sampling_rate=_get_config_value(linten_params, optional_params, "streaming_sampling_rate") or 5,
        fail_open=_get_config_value(linten_params, optional_params, "fail_open"),
        guardrail_timeout=_get_config_value(linten_params, optional_params, "guardrail_timeout"),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )

    linten.logging_callback_manager.add_linten_callback(grayswan_guardrail)
    return grayswan_guardrail


def _get_config_value(linten_params, optional_params, attribute_name):
    if optional_params is not None:
        value: Final = getattr(optional_params, attribute_name, None)
        if value is not None:
            return value
    return getattr(linten_params, attribute_name, None)


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.GRAYSWAN.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.GRAYSWAN.value: GraySwanGuardrail,
}


__all__ = [
    "GraySwanGuardrail",
    "GraySwanGuardrailAPIError",
    "GraySwanGuardrailMissingSecrets",
    "initialize_guardrail",
]
