from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .model_armor import ModelArmorGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten
    from linten.proxy.guardrails.guardrail_hooks.model_armor import (
        ModelArmorGuardrail,
    )

    _model_armor_callback: Final = ModelArmorGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        template_id=linten_params.template_id,
        project_id=linten_params.project_id,
        location=linten_params.location,
        credentials=linten_params.credentials,
        api_endpoint=linten_params.api_endpoint,
        default_on=linten_params.default_on,
        mask_request_content=linten_params.mask_request_content,
        mask_response_content=linten_params.mask_response_content,
        fail_on_error=linten_params.fail_on_error,
        skip_unscannable_attachments=linten_params.skip_unscannable_attachments,
        sanitize_error_detail=linten_params.sanitize_error_detail,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_model_armor_callback)

    return _model_armor_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.MODEL_ARMOR.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.MODEL_ARMOR.value: ModelArmorGuardrail,
}
