from __future__ import annotations

from typing import TYPE_CHECKING, Final

from pydantic import BaseModel

from linten.types.guardrails import (
    GuardrailEventHooks,
    Mode,
    SupportedGuardrailIntegrations,
)
from linten.types.proxy.guardrails.guardrail_hooks.typesafe import (
    TypeSafeGuardrailOptionalParams,
)

from .typesafe import TypeSafeGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams


def _coerce_event_hook(
    mode: str | list[str] | Mode,
) -> GuardrailEventHooks | list[GuardrailEventHooks] | Mode:
    if isinstance(mode, Mode):
        return mode
    if isinstance(mode, list):
        return [GuardrailEventHooks(item) for item in mode]
    return GuardrailEventHooks(mode)


def _optional_params(linten_params: LintenParams) -> TypeSafeGuardrailOptionalParams:
    value: Final = linten_params.optional_params
    if isinstance(value, TypeSafeGuardrailOptionalParams):
        return value
    if isinstance(value, BaseModel):
        return TypeSafeGuardrailOptionalParams.model_validate(value.model_dump())
    return TypeSafeGuardrailOptionalParams()


def initialize_guardrail(linten_params: LintenParams, guardrail: Guardrail) -> TypeSafeGuardrail:
    import linten

    optional_params: Final = _optional_params(linten_params)

    _callback: Final = TypeSafeGuardrail(
        api_base=linten_params.api_base,
        api_key=linten_params.api_key,
        model=linten_params.model,
        relevance_threshold=optional_params.relevance_threshold,
        min_chars_to_evaluate=optional_params.min_chars_to_evaluate,
        max_result_chars_in_state=optional_params.max_result_chars_in_state,
        guardrail_name=guardrail["guardrail_name"],
        event_hook=_coerce_event_hook(linten_params.mode),
        default_on=linten_params.default_on or False,
        timeout=linten_params.timeout,
        unreachable_fallback=(
            linten_params.unreachable_fallback if "unreachable_fallback" in linten_params.model_fields_set else None
        ),
    )
    linten.logging_callback_manager.add_linten_callback(  # pyright: ignore[reportUnknownMemberType]  # callback manager is untyped
        _callback
    )
    return _callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.TYPESAFE.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.TYPESAFE.value: TypeSafeGuardrail,
}
