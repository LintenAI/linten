from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .qualifire import QualifireGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _qualifire_callback: Final = QualifireGuardrail(
        api_key=linten_params.api_key,
        api_base=linten_params.api_base,
        evaluation_id=getattr(linten_params, "evaluation_id", None),
        prompt_injections=getattr(linten_params, "prompt_injections", None),
        hallucinations_check=getattr(linten_params, "hallucinations_check", None),
        grounding_check=getattr(linten_params, "grounding_check", None),
        pii_check=getattr(linten_params, "pii_check", None),
        content_moderation_check=getattr(linten_params, "content_moderation_check", None),
        tool_selection_quality_check=getattr(linten_params, "tool_selection_quality_check", None),
        assertions=getattr(linten_params, "assertions", None),
        on_flagged=getattr(linten_params, "on_flagged", "block"),
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )

    linten.logging_callback_manager.add_linten_callback(_qualifire_callback)

    return _qualifire_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.QUALIFIRE.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.QUALIFIRE.value: QualifireGuardrail,
}
