from typing import TYPE_CHECKING, Final, Literal, Optional

import linten
from linten.proxy.guardrails.guardrail_hooks.mcp_security.mcp_security_guardrail import (
    MCPSecurityGuardrail,
)
from linten.types.guardrails import SupportedGuardrailIntegrations

if TYPE_CHECKING:
    from linten import Router
    from linten.types.guardrails import Guardrail, LintenParams


def initialize_guardrail(
    linten_params: "LintenParams",
    guardrail: "Guardrail",
    llm_router: Optional["Router"] = None,
):
    guardrail_name: Final = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("MCP Security: guardrail_name is required")

    on_violation: Final[Literal["block", "alert"]] = "block" if linten_params.on_violation == "block" else "alert"

    mcp_security_guardrail: Final = MCPSecurityGuardrail(
        guardrail_name=guardrail_name,
        event_hook=linten_params.mode,
        default_on=linten_params.default_on or False,
        on_violation=on_violation,
    )

    linten.logging_callback_manager.add_linten_callback(mcp_security_guardrail)
    return mcp_security_guardrail


guardrail_initializer_registry: Final = {
    SupportedGuardrailIntegrations.MCP_SECURITY.value: initialize_guardrail,
}

guardrail_class_registry: Final = {
    SupportedGuardrailIntegrations.MCP_SECURITY.value: MCPSecurityGuardrail,
}
