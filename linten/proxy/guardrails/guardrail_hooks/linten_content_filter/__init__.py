from typing import TYPE_CHECKING, Final, Optional

import linten
from linten.proxy.guardrails.guardrail_hooks.linten_content_filter.content_filter import (
    ContentFilterGuardrail,
)
from linten.types.guardrails import SupportedGuardrailIntegrations

if TYPE_CHECKING:
    from linten import Router
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(
    linten_params: "LintenParams",
    guardrail: "Guardrail",
    llm_router: Optional["Router"] = None,
):
    """
    Initialize the Content Filter Guardrail.

    Args:
        linten_params: Guardrail configuration parameters
        guardrail: Guardrail metadata

    Returns:
        Initialized ContentFilterGuardrail instance
    """
    guardrail_name: Final = guardrail.get("guardrail_name")

    if not guardrail_name:
        raise ValueError("Content Filter: guardrail_name is required")

    content_filter_guardrail: Final = ContentFilterGuardrail(
        guardrail_name=guardrail_name,
        guardrail_id=guardrail.get("guardrail_id"),
        policy_template=guardrail.get("policy_template"),
        patterns=linten_params.patterns,
        blocked_words=linten_params.blocked_words,
        blocked_words_file=linten_params.blocked_words_file,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on or False,
        categories=getattr(linten_params, "categories", None),
        severity_threshold=getattr(linten_params, "severity_threshold", "medium"),
        llm_router=llm_router,
        image_model=getattr(linten_params, "image_model", None),
        competitor_intent_config=getattr(linten_params, "competitor_intent_config", None),
        end_session_after_n_fails=getattr(linten_params, "end_session_after_n_fails", None),
        on_violation=getattr(linten_params, "on_violation", None),
        realtime_violation_message=getattr(linten_params, "realtime_violation_message", None),
    )

    linten.logging_callback_manager.add_linten_callback(content_filter_guardrail)

    return content_filter_guardrail


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.LINTEN_CONTENT_FILTER.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.LINTEN_CONTENT_FILTER.value: ContentFilterGuardrail,
}
