from datetime import datetime

from pydantic import Field
from typing_extensions import TypedDict

from linten.types.llms.base import LintenBaseModel


class MCPToolsetTool(TypedDict):
    server_id: str
    tool_name: str


class MCPToolset(LintenBaseModel):
    toolset_id: str
    toolset_name: str
    description: str | None = None
    tools: list[MCPToolsetTool] = Field(default=[])
    created_at: datetime | None = None
    created_by: str | None = None
    updated_at: datetime | None = None
    updated_by: str | None = None


class NewMCPToolsetRequest(LintenBaseModel):
    toolset_name: str
    description: str | None = None
    tools: list[MCPToolsetTool] = Field(default=[])


class UpdateMCPToolsetRequest(LintenBaseModel):
    toolset_id: str
    toolset_name: str | None = None
    description: str | None = None
    tools: list[MCPToolsetTool] | None = None
