from typing import TYPE_CHECKING, Final, Literal

from pydantic import field_validator

import linten
from linten._logging import verbose_proxy_logger
from linten.types.guardrails import SupportedGuardrailIntegrations
from linten.types.llms.base import LintenBaseModel

from .straiker import StraikerGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


class _V3Routing(LintenBaseModel):
    api_version: Literal["v1", "v3"] | None = None
    agent_ref: str | None = None
    client: str | None = None
    format_hint: Literal["anthropic.messages", "openai.chat"] | None = None

    @field_validator("api_version", mode="before")
    @classmethod
    def _unknown_api_version_is_unset(cls, value: object) -> object:
        if value is None or value in ("v1", "v3"):
            return value
        verbose_proxy_logger.warning(
            "Straiker guardrail: ignoring api_version %r, expected 'v1', 'v3' or unset; "
            "the route follows the api_key prefix",
            value,
        )
        return None


_OPTIONAL_INIT_FIELDS: Final = (
    "timeout",
    "max_retries",
    "initial_backoff",
    "max_backoff",
    "unreachable_fallback",
    "fail_on_error",
    "max_payload_bytes",
    "custom_headers",
    "metadata",
    "verbose",
)


def _get_config_value(linten_params: "LintenParams", optional_params: object, attribute_name: str) -> object:
    if optional_params is not None:
        if isinstance(optional_params, dict):
            value = optional_params.get(attribute_name)
        else:
            value = getattr(optional_params, attribute_name, None)
        if value is not None:
            return value
    return getattr(linten_params, attribute_name, None)


def initialize_guardrail(linten_params: "LintenParams", guardrail: "Guardrail"):
    optional_params: Final = getattr(linten_params, "optional_params", None)
    api_key: Final = linten_params.api_key
    if not api_key:
        raise ValueError("api_key is required for straiker")

    api_base: Final = linten_params.api_base or "https://api.prod.straiker.ai"
    default_app: Final = getattr(linten_params, "default_app", None) or getattr(linten_params, "source", None)
    source: Final = default_app if isinstance(default_app, str) and default_app else "Linten Gateway"
    kwargs: Final[dict[str, object]] = {
        field: value
        for field in _OPTIONAL_INIT_FIELDS
        for value in [_get_config_value(linten_params, optional_params, field)]
        if value is not None
    }
    routing: Final = _V3Routing.model_validate(
        {
            field: _get_config_value(linten_params, optional_params, field)
            for field in ("api_version", "agent_ref", "client", "format_hint")
        }
    )
    _callback: Final = StraikerGuardrail(
        api_key=api_key,
        api_base=api_base if isinstance(api_base, str) else "https://api.prod.straiker.ai",
        source=source,
        guardrail_name=guardrail.get("guardrail_name", "straiker"),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
        api_version=routing.api_version,
        agent_ref=routing.agent_ref,
        client=routing.client,
        format_hint=routing.format_hint,
        **kwargs,
    )

    linten.logging_callback_manager.add_linten_callback(_callback)
    return _callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.STRAIKER.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.STRAIKER.value: StraikerGuardrail,
}
