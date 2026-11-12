"""
Tag table model.

Canonical definition for ``linten_tagtable``. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from datetime import datetime

from pydantic import model_validator

from linten.models.budget import Linten_BudgetTable
from linten.types.llms.base import LintenPydanticObjectBase


class Linten_TagTable(LintenPydanticObjectBase):
    tag_name: str
    description: str | None = None
    models: list[str] = []
    model_info: dict | None = None
    spend: float = 0.0
    budget_id: str | None = None
    linten_budget_table: Linten_BudgetTable | None = None
    created_at: datetime | None = None
    created_by: str | None = None
    updated_at: datetime | None = None

    @model_validator(mode="before")
    @classmethod
    def set_model_info(cls, values):
        if values.get("spend") is None:
            values.update({"spend": 0.0})
        if values.get("models") is None:
            values.update({"models": []})
        return values
