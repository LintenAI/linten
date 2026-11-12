"""
End-user table model.

Canonical definition for ``linten_endusertable``. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from typing import Literal

from pydantic import ConfigDict, Field, field_validator

from linten.models.budget import Linten_BudgetTable
from linten.models.object_permission import Linten_ObjectPermissionTable
from linten.types.llms.base import LintenPydanticObjectBase


class Linten_EndUserTable(LintenPydanticObjectBase):
    user_id: str
    blocked: bool
    alias: str | None = None
    spend: float = 0.0
    allowed_model_region: Literal["eu", "us"] | None = None
    default_model: str | None = None
    models: list[str] = Field(default_factory=list)
    budget_id: str | None = None
    linten_budget_table: Linten_BudgetTable | None = None
    object_permission_id: str | None = None
    object_permission: Linten_ObjectPermissionTable | None = None

    @field_validator("spend", mode="before")
    @classmethod
    def default_null_spend_to_zero(cls, spend: object) -> object:
        return 0.0 if spend is None else spend

    model_config = ConfigDict(protected_namespaces=())
