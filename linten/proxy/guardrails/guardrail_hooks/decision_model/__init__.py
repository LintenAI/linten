from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Final

from pydantic import TypeAdapter, ValidationError

from linten.types.guardrails import (
    GuardrailEventHooks,
    Mode,
    SupportedGuardrailIntegrations,
)
from linten.types.proxy.guardrails.guardrail_hooks.decision_model import (
    DecisionModelCheck,
)

from .decision_model import DecisionModelGuardrail

if TYPE_CHECKING:
    from linten.types.guardrails import Guardrail, LintenParams

_CHECKS_ADAPTER: Final = TypeAdapter(list[DecisionModelCheck])


def _coerce_event_hook(
    mode: str | Sequence[str] | Mode,
) -> GuardrailEventHooks | tuple[GuardrailEventHooks, ...] | Mode:
    if isinstance(mode, Mode):
        return mode
    if isinstance(mode, str):
        return GuardrailEventHooks(mode)
    return tuple(GuardrailEventHooks(item) for item in mode)


def _parse_checks(raw_checks: object) -> tuple[DecisionModelCheck, ...]:
    try:
        checks: Final = _CHECKS_ADAPTER.validate_python(raw_checks)
    except ValidationError as error:
        raise ValueError(f"decision_model guardrail has invalid checks: {error}") from error
    return tuple(checks)


def _streaming_end_of_stream_only(linten_params: LintenParams) -> bool:
    value: Final[object] = getattr(linten_params, "streaming_end_of_stream_only", None)
    if value is None:
        return False
    if not isinstance(value, bool):
        raise TypeError(f"decision_model guardrail streaming_end_of_stream_only must be a boolean, got {value!r}")
    return value


def _streaming_sampling_rate(linten_params: LintenParams) -> int:
    value: Final[object] = getattr(linten_params, "streaming_sampling_rate", None)
    if value is None:
        return 5
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"decision_model guardrail streaming_sampling_rate must be an integer, got {value!r}")
    if value < 1:
        raise ValueError(f"decision_model guardrail streaming_sampling_rate must be at least 1, got {value}")
    return value


def _streaming_buffer_until_moderated(linten_params: LintenParams) -> bool | None:
    value: Final[object] = getattr(linten_params, "streaming_buffer_until_moderated", None)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise TypeError(f"decision_model guardrail streaming_buffer_until_moderated must be a boolean, got {value!r}")
    return value


def initialize_guardrail(linten_params: LintenParams, guardrail: Guardrail) -> DecisionModelGuardrail:
    import linten

    decision_model: Final = linten_params.decision_model
    if not decision_model:
        raise ValueError("decision_model guardrail requires decision_model in linten_params")

    checks: Final = _parse_checks(linten_params.checks)

    _callback: Final = DecisionModelGuardrail(
        guardrail_name=guardrail["guardrail_name"],
        decision_model=decision_model,
        checks=checks,
        event_hook=_coerce_event_hook(linten_params.mode),
        default_on=linten_params.default_on or False,
        unreachable_fallback=(
            linten_params.unreachable_fallback
            if "unreachable_fallback" in linten_params.model_fields_set
            else "fail_closed"
        ),
        max_input_chars=linten_params.max_input_chars or 24000,
        timeout=linten_params.timeout,
        max_concurrent_decision_calls=linten_params.max_concurrent_decision_calls or 8,
        streaming_end_of_stream_only=_streaming_end_of_stream_only(linten_params),
        streaming_sampling_rate=_streaming_sampling_rate(linten_params),
        streaming_buffer_until_moderated=_streaming_buffer_until_moderated(linten_params),
    )
    linten.logging_callback_manager.add_linten_callback(  # pyright: ignore[reportUnknownMemberType]  # callback manager is untyped
        _callback
    )
    return _callback


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.DECISION_MODEL.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.DECISION_MODEL.value: DecisionModelGuardrail,
}


__all__ = [
    "DecisionModelGuardrail",
    "guardrail_class_registry",
    "guardrail_initializer_registry",
    "initialize_guardrail",
]
