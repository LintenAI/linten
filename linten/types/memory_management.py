"""
Pydantic models for Memory management endpoints.
"""

from datetime import datetime

from pydantic import Field

from linten.types.llms.base import LintenBaseModel


class Linten_MemoryRow(LintenBaseModel):
    memory_id: str
    key: str
    value: str
    metadata: object | None = None
    user_id: str | None = None
    team_id: str | None = None
    created_at: datetime | None = None
    created_by: str | None = None
    updated_at: datetime | None = None
    updated_by: str | None = None


class MemoryCreateRequest(LintenBaseModel):
    key: str = Field(..., description="Memory key (acts as the namespace in the URL).")
    value: str = Field(..., description="Memory content. Typically markdown/text for LLM context.")
    metadata: object | None = Field(
        default=None,
        description="Optional JSON metadata (tags, structured fields).",
    )
    user_id: str | None = Field(
        default=None,
        description="Scope to this user. Defaults to the caller's user_id.",
    )
    team_id: str | None = Field(
        default=None,
        description="Scope to this team. Defaults to the caller's team_id.",
    )


class MemoryUpdateRequest(LintenBaseModel):
    value: str | None = None
    metadata: object | None = None
    # Only honored on create (when the row doesn't yet exist) and only for
    # PROXY_ADMIN callers — mirrors MemoryCreateRequest so admins can bootstrap
    # rows scoped to another user/team via PUT, not just POST.
    user_id: str | None = None
    team_id: str | None = None


class MemoryListResponse(LintenBaseModel):
    memories: list[Linten_MemoryRow]
    total: int


class MemoryDeleteResponse(LintenBaseModel):
    key: str
    deleted: bool
