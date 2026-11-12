from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from linten.types.guardrails import SupportedGuardrailIntegrations

from .conduct import ConductGuardrail

if TYPE_CHECKING:
    from linten.integrations.custom_guardrail import CustomGuardrail
    from linten.types.guardrails import Guardrail, LintenParams

DEFAULT_TIMEOUT_SECONDS: Final = 8.0
_NO_EXTRAS: Final[Mapping[str, object]] = MappingProxyType({})


def initialize_guardrail(
    linten_params: LintenParams,
    guardrail: Guardrail,
    guardrail_cls: type[CustomGuardrail] = ConductGuardrail,
) -> CustomGuardrail:
    import linten

    extras: Final = linten_params.model_extra or _NO_EXTRAS
    _callback: Final = guardrail_cls(
        api_url=linten_params.api_base,
        agent_token=linten_params.api_key,
        workspace_id=extras.get("workspace_id"),
        tool_name=extras.get("tool_name", "llm_call"),
        unreachable_fallback=linten_params.unreachable_fallback,
        timeout=DEFAULT_TIMEOUT_SECONDS if linten_params.timeout is None else linten_params.timeout,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        supported_event_hooks=guardrail_cls.get_supported_event_hooks(),
    )
    linten.logging_callback_manager.add_linten_callback(_callback)
    return _callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.CONDUCT.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.CONDUCT.value: ConductGuardrail,
}
