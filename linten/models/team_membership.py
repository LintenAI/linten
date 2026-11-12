"""
Team membership table model.

Canonical definition for ``linten_teammembership``. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from linten.models.budget import Linten_BudgetTable, Linten_BudgetTableFull
from linten.types.llms.base import LintenPydanticObjectBase


class Linten_TeamMembership(LintenPydanticObjectBase):
    user_id: str
    team_id: str
    budget_id: str | None = None
    spend: float | None = 0.0
    total_spend: float | None = 0.0
    linten_budget_table: Linten_BudgetTableFull | Linten_BudgetTable | None = None

    def safe_get_team_member_rpm_limit(self) -> int | None:
        if self.linten_budget_table is not None:
            return self.linten_budget_table.rpm_limit
        return None

    def safe_get_team_member_tpm_limit(self) -> int | None:
        if self.linten_budget_table is not None:
            return self.linten_budget_table.tpm_limit
        return None
