"""Custom code guardrail integration for Linten.

This module allows users to write custom guardrail logic using Python-like code
that runs in a sandboxed environment with access to Linten-provided primitives.

Pre-built custom code for common guardrails (e.g. response rejection detection)
is available in response_rejection_code.py.
"""

from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .custom_code_guardrail import CustomCodeGuardrail
from .response_rejection_code import (
    DEFAULT_REJECTION_PHRASES,
    RESPONSE_REJECTION_GUARDRAIL_CODE,
)

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail") -> CustomCodeGuardrail:
    """
    Initialize a custom code guardrail.

    Args:
        linten_params: Configuration parameters including the custom code
        guardrail: The guardrail configuration dict

    Returns:
        CustomCodeGuardrail instance
    """
    import linten

    guardrail_name: Final = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Custom code guardrail requires a guardrail_name")

    # Get the custom code from linten_params
    custom_code: Final = linten_params.custom_code
    if not custom_code:
        raise ValueError("Custom code guardrail requires 'custom_code' in linten_params")

    custom_code_guardrail: Final = CustomCodeGuardrail(
        guardrail_name=guardrail_name,
        custom_code=custom_code,
        execution_timeout=linten_params.timeout,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )

    linten.logging_callback_manager.add_linten_callback(custom_code_guardrail)
    return custom_code_guardrail


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.CUSTOM_CODE.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.CUSTOM_CODE.value: CustomCodeGuardrail,
}

__all__ = [
    "DEFAULT_REJECTION_PHRASES",
    "RESPONSE_REJECTION_GUARDRAIL_CODE",
    "CustomCodeGuardrail",
    "initialize_guardrail",
]
