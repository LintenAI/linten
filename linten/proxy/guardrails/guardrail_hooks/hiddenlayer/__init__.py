from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .hiddenlayer import HiddenlayerGuardrail, HiddenlayerGuardrailV2

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    api_id: Final = linten_params.api_id if hasattr(linten_params, "api_id") else None
    auth_url: Final = linten_params.auth_url if hasattr(linten_params, "auth_url") else None
    version: Final[int | None] = linten_params.version if hasattr(linten_params, "version") else None

    _hiddenlayer_callback: HiddenlayerGuardrail | HiddenlayerGuardrailV2
    if not version or version < 2:
        _hiddenlayer_callback = HiddenlayerGuardrail(
            api_base=linten_params.api_base,
            api_id=api_id,
            api_key=linten_params.api_key,
            auth_url=auth_url,
            guardrail_name=guardrail.get("guardrail_name", ""),
            event_hook=linten_params.mode,
            default_on=linten_params.default_on,
            timeout=linten_params.timeout,
        )
    else:
        _hiddenlayer_callback = HiddenlayerGuardrailV2(
            api_base=linten_params.api_base,
            api_id=api_id,
            api_key=linten_params.api_key,
            auth_url=auth_url,
            guardrail_name=guardrail.get("guardrail_name", ""),
            event_hook=linten_params.mode,
            default_on=linten_params.default_on,
            timeout=linten_params.timeout,
        )

    linten.logging_callback_manager.add_linten_callback(_hiddenlayer_callback)
    return _hiddenlayer_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.HIDDENLAYER.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.HIDDENLAYER.value: HiddenlayerGuardrail,
}
