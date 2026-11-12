"""
Object permission table model.

Canonical definition for ``linten_objectpermissiontable``. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from linten.types.llms.base import LintenPydanticObjectBase


class Linten_ObjectPermissionTable(LintenPydanticObjectBase):
    """Represents a Linten_ObjectPermissionTable record"""

    object_permission_id: str
    mcp_servers: list[str] | None = []
    mcp_access_groups: list[str] | None = []
    mcp_tool_permissions: dict[str, list[str]] | None = None
    vector_stores: list[str] | None = []
    agents: list[str] | None = []
    agent_access_groups: list[str] | None = []
    models: list[str] | None = []
    mcp_toolsets: list[str] | None = None
    blocked_tools: list[str] | None = []
    search_tools: list[str] | None = []
    mcp_tool_search_enabled: bool | None = None
    skills: list[str] | None = None
