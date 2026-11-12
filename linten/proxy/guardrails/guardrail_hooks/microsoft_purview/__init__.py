from typing import TYPE_CHECKING, Final

from linten.linten_core_utils.core_helpers import attribute_or_none
from linten.types.guardrails import SupportedGuardrailIntegrations

from .purview_dlp import MicrosoftPurviewDLPGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    tenant_id: Final = attribute_or_none(linten_params, "tenant_id")
    client_id: Final = attribute_or_none(linten_params, "client_id")

    # client_secret can be passed via the standard api_key field or as
    # a dedicated client_secret parameter.
    client_secret: Final = linten_params.api_key or getattr(linten_params, "client_secret", None)

    if not tenant_id:
        raise ValueError("Microsoft Purview: tenant_id is required")
    if not client_id:
        raise ValueError("Microsoft Purview: client_id is required")
    if not client_secret:
        raise ValueError("Microsoft Purview: client_secret (or api_key) is required")

    guardrail_name: Final = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Microsoft Purview: guardrail_name is required")

    purview_guardrail: Final = MicrosoftPurviewDLPGuardrail(
        guardrail_name=guardrail_name,
        tenant_id=str(tenant_id),
        client_id=str(client_id),
        client_secret=str(client_secret),
        purview_app_name=str(getattr(linten_params, "purview_app_name", None) or "Linten"),
        user_id_field=str(getattr(linten_params, "user_id_field", None) or "user_id"),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        timeout=linten_params.timeout,
    )

    linten.logging_callback_manager.add_linten_callback(purview_guardrail)
    return purview_guardrail


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.MICROSOFT_PURVIEW.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.MICROSOFT_PURVIEW.value: MicrosoftPurviewDLPGuardrail,
}
