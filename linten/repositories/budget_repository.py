"""
Budget repository for database operations on Linten_BudgetTable.
"""

from collections.abc import Mapping
from typing import TYPE_CHECKING, Final

from linten.models.budget import Linten_BudgetTable
from linten.repositories.base_repository import BaseRepository
from linten.repositories.prisma_protocols import TableActions
from linten.repositories.table_repositories import PrismaTableRepository

if TYPE_CHECKING:
    from prisma import models as prisma_models


class _BudgetTable(PrismaTableRepository["prisma_models.Linten_BudgetTable"]):
    table_name = "linten_budgettable"


class BudgetRepository(BaseRepository[Linten_BudgetTable]):
    """Repository for budget database operations."""

    @property
    def table(self) -> TableActions["prisma_models.Linten_BudgetTable"]:
        return _BudgetTable(self._prisma_client).table

    @property
    def model_class(self) -> type[Linten_BudgetTable]:
        return Linten_BudgetTable

    async def find_by_id(self, budget_id: str, id_field: str = "budget_id") -> Linten_BudgetTable | None:
        return await super().find_by_id(budget_id, id_field)

    async def create_budget(
        self,
        created_by: str,
        max_budget: float | None = None,
        soft_budget: float | None = None,
        max_parallel_requests: int | None = None,
        tpm_limit: int | None = None,
        rpm_limit: int | None = None,
        model_max_budget: Mapping[str, object] | None = None,
        budget_duration: str | None = None,
        allowed_models: list[str] | None = None,
    ) -> Linten_BudgetTable:
        """Create a new budget record."""
        data: Final[dict[str, object]] = {
            "created_by": created_by,
            "updated_by": created_by,
        }
        if max_budget is not None:
            data["max_budget"] = max_budget
        if soft_budget is not None:
            data["soft_budget"] = soft_budget
        if max_parallel_requests is not None:
            data["max_parallel_requests"] = max_parallel_requests
        if tpm_limit is not None:
            data["tpm_limit"] = tpm_limit
        if rpm_limit is not None:
            data["rpm_limit"] = rpm_limit
        if model_max_budget is not None:
            data["model_max_budget"] = model_max_budget
        if budget_duration is not None:
            data["budget_duration"] = budget_duration
        if allowed_models is not None:
            data["allowed_models"] = allowed_models

        return await self.create(data)

    async def update_budget(
        self,
        budget_id: str,
        updated_by: str,
        max_budget: float | None = None,
        soft_budget: float | None = None,
        max_parallel_requests: int | None = None,
        tpm_limit: int | None = None,
        rpm_limit: int | None = None,
        model_max_budget: Mapping[str, object] | None = None,
        budget_duration: str | None = None,
        allowed_models: list[str] | None = None,
    ) -> Linten_BudgetTable | None:
        """Update an existing budget record."""
        data: Final[dict[str, object]] = {"updated_by": updated_by}
        if max_budget is not None:
            data["max_budget"] = max_budget
        if soft_budget is not None:
            data["soft_budget"] = soft_budget
        if max_parallel_requests is not None:
            data["max_parallel_requests"] = max_parallel_requests
        if tpm_limit is not None:
            data["tpm_limit"] = tpm_limit
        if rpm_limit is not None:
            data["rpm_limit"] = rpm_limit
        if model_max_budget is not None:
            data["model_max_budget"] = model_max_budget
        if budget_duration is not None:
            data["budget_duration"] = budget_duration
        if allowed_models is not None:
            data["allowed_models"] = allowed_models

        return await self.update(budget_id, data, id_field="budget_id")

    async def delete_budget(self, budget_id: str) -> Linten_BudgetTable | None:
        """Delete a budget record."""
        return await self.delete(budget_id, id_field="budget_id")
