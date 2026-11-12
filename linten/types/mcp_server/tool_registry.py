from collections.abc import Callable
from typing import ClassVar

from pydantic import ConfigDict, Field

from linten.types.llms.base import LintenBaseModel


class MCPTool(LintenBaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)
    name: str
    description: str
    input_schema: dict[str, object]
    handler: Callable
    server_id: str | None = Field(default=None, frozen=True)


class ToolSchema(LintenBaseModel):
    name: str
    description: str
    inputSchema: dict[str, object]


class ListToolsResponse(LintenBaseModel):
    tools: list[ToolSchema]
    nextCursor: str | None = None
    _meta: dict[str, object] | None = None


class CallToolRequest(LintenBaseModel):
    method: str = "tools/call"
    params: dict[str, object]


class ContentItem(LintenBaseModel):
    type: str
    text: str | None = None
