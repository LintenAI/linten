from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .cato_networks import CatoNetworksGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten
    from linten.proxy.guardrails.guardrail_hooks.cato_networks import (
        CatoNetworksGuardrail,
    )

    _cato_callback: Final = CatoNetworksGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        inspect_embeddings=linten_params.inspect_embeddings,
        ssl_verify=getattr(linten_params, "ssl_verify", None),
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_cato_callback)

    return _cato_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.CATO_NETWORKS.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.CATO_NETWORKS.value: CatoNetworksGuardrail,
}
