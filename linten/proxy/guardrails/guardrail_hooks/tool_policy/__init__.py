from typing import Final

import linten
from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(linten_params: LintenParams, guardrail: Guardrail):
    from linten.proxy.guardrails.guardrail_hooks.tool_policy.tool_policy_guardrail import (
        ToolPolicyGuardrail,
    )

    _callback: Final = ToolPolicyGuardrail(
        guardrail_name=guardrail.get("guardrail_name", "tool_policy"),
        event_hook=linten_params.mode,
        default_on=linten_params.default_on,
    )
    linten.logging_callback_manager.add_linten_callback(_callback)
    return _callback
