from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .prompt_security import PromptSecurityGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten
    from linten.proxy.guardrails.guardrail_hooks.prompt_security import (
        PromptSecurityGuardrail,
    )

    _prompt_security_callback: Final = PromptSecurityGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        streaming_transform_mode=getattr(linten_params, "streaming_transform_mode", None),
        file_sanitization_fail_open=getattr(linten_params, "file_sanitization_fail_open", None),
        block_on_file_modify=getattr(linten_params, "block_on_file_modify", None),
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_prompt_security_callback)

    return _prompt_security_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.PROMPT_SECURITY.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.PROMPT_SECURITY.value: PromptSecurityGuardrail,
}
