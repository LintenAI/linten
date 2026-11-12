"""
Organization table model.

Canonical definition for ``linten_organizationtable``. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from linten.models.budget import Linten_BudgetTable
from linten.models.object_permission import Linten_ObjectPermissionTable
from linten.models.user import Linten_UserTable
from linten.types.llms.base import LintenPydanticObjectBase


class Linten_OrganizationTable(LintenPydanticObjectBase):
    """Represents user-controllable params for a Linten_OrganizationTable record"""

    organization_id: str | None = None
    organization_alias: str | None = None
    budget_id: str
    spend: float = 0.0
    metadata: dict | None = None
    models: list[str] = []
    model_spend: dict | None = {}
    created_by: str
    updated_by: str
    users: list[Linten_UserTable] | None = None
    linten_budget_table: Linten_BudgetTable | None = None
    object_permission: Linten_ObjectPermissionTable | None = None
    object_permission_id: str | None = None
