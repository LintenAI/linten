from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .javelin import JavelinGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    import linten

    if linten_params.guard_name is None:
        raise Exception(
            "JavelinGuardrailException - Please pass the Javelin guard name via 'linten_params::guard_name'"
        )

    _javelin_callback: Final = JavelinGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        javelin_guard_name=linten_params.guard_name,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on or False,
        api_version=linten_params.api_version or "v1",
        config=linten_params.config,
        metadata=linten_params.metadata,
        application=linten_params.application,
        timeout=linten_params.timeout,
    )
    linten.logging_callback_manager.add_linten_callback(_javelin_callback)

    return _javelin_callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.JAVELIN.value: initialize_guardrail,
}


guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.JAVELIN.value: JavelinGuardrail,
}
