from pydantic import Field

from linten.models.budget import Linten_BudgetTableFull
from linten.models.end_user import Linten_EndUserTable
from linten.types.llms.base import LintenBaseModel


class CustomerResponse(Linten_EndUserTable):
    """Customer object returned by the /customer read+write endpoints.

    Nests the full budget response model so server-managed budget fields
    (budget_reset_at, created_at) survive response_model filtering, rather than
    the narrow write-allowlist shape Linten_EndUserTable carries for internal use.
    """

    linten_budget_table: Linten_BudgetTableFull | None = None  # pyright: ignore


class BlockUsersResponse(LintenBaseModel):
    blocked_users: list[Linten_EndUserTable]


class UnblockUsersResponse(LintenBaseModel):
    blocked_users: list[str] = Field(description="User IDs that remain blocked after this unblock call")


class DeleteCustomersResponse(LintenBaseModel):
    deleted_customers: int
    message: str
