from collections.abc import Mapping, Sequence
from typing import Literal

from pydantic import Field

from linten.types.llms.base import LintenBaseModel

from .base import GuardrailConfigModel


class ContentBlock(LintenBaseModel):
    type: str | None = None
    text: str | None = None


class ToolCallFunction(LintenBaseModel):
    name: str
    arguments: str


class ToolCall(LintenBaseModel):
    id: str
    type: str = "function"
    function: ToolCallFunction


class AssistantMessage(LintenBaseModel):
    role: Literal["assistant"] = "assistant"
    content: str | Sequence[ContentBlock] | None = None
    tool_calls: Sequence[ToolCall] | None = None


class SingulrGuardrailPayload(LintenBaseModel):
    correlation_id: str | None = None
    model_name: str | None = None
    model_provider_name: str | None = None
    guardrail_scope: str | None = None
    messages: Sequence[Mapping[str, object]] | None = None
    images: Sequence[str] | None = None
    tools: Sequence[Mapping[str, object]] | None = None
    response: AssistantMessage | None = None
    metadata: Mapping[str, str] | None = None


class SingulrMcpGuardrailPayload(LintenBaseModel):
    model_name: str | None = None
    guardrail_scope: str | None = None
    tool_name: str | None = None
    tool_arguments: object = None
    mcp_server_name: str | None = None
    tool_result: Sequence[str] | None = None
    metadata: Mapping[str, str] | None = None


class SingulrGuardrailResponse(LintenBaseModel):
    """Response returned by the Singulr guardrail API."""

    should_block: bool = False
    blocking_due_to: str | None = None


class SingulrGuardrailConfigModel(GuardrailConfigModel):
    singulr_api_key: str | None = Field(
        default=None,
        description="The Singulr API key. Generate API key from Singulr Platform.",
    )

    singulr_api_base: str | None = Field(
        default=None,
        description="The Singulr API base URL. Get base URL from Singulr Platform.",
    )

    singulr_application_id: str | None = Field(
        default=None,
        description="The Singulr application ID. Get application ID from Singulr Platform.",
    )

    singulr_guardrail_id: str | None = Field(
        default=None,
        description="The Singulr Guardrail ID. Get guardrail ID from Singulr Platform.",
    )

    block_on_error: bool | None = Field(
        default=None,
        description=(
            "Whether to block requests when the Singulr Guardrails API is unavailable "
            "or returns an error. If enabled, requests fail closed. "
            "If disabled, requests continue without guardrail enforcement (fail open)."
        ),
    )

    @staticmethod
    def ui_friendly_name() -> str:
        return "Singulr"
