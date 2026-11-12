from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .zscaler_ai_guard import ZscalerAIGuard

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    _zscaler_ai_guard_callback: Final = ZscalerAIGuard(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        policy_id=linten_params.policy_id,
        send_user_api_key_alias=linten_params.send_user_api_key_alias,
        send_user_api_key_user_id=linten_params.send_user_api_key_user_id,
        send_user_api_key_team_id=linten_params.send_user_api_key_team_id,
        timeout=linten_params.timeout,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )
    linten.logging_callback_manager.add_linten_callback(_zscaler_ai_guard_callback)

    return _zscaler_ai_guard_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.ZSCALER_AI_GUARD.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.ZSCALER_AI_GUARD.value: ZscalerAIGuard,
}
