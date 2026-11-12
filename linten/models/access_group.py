"""
Access group table model.

Canonical definition for ``linten_accessgrouptable``. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from collections.abc import Mapping, Sequence
from datetime import datetime

from linten.types.llms.base import LintenPydanticObjectBase


class Linten_AccessGroupTable(LintenPydanticObjectBase):
    access_group_id: str
    access_group_name: str
    description: str | None = None
    access_model_names: list[str] = []
    access_mcp_server_ids: list[str] = []
    mcp_tool_permissions: Mapping[str, Sequence[str]] | None = None
    access_agent_ids: list[str] = []
    access_skill_names: tuple[str, ...] = ()
    assigned_team_ids: list[str] = []
    assigned_key_ids: list[str] = []
    created_at: datetime | None = None
    created_by: str | None = None
    updated_at: datetime | None = None
    updated_by: str | None = None
