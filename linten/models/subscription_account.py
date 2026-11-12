"""
Subscription account table model.

Canonical definition for ``linten_subscriptionaccounttable``: the operator-entered
recurring fee of a provider account whose requests are covered by a flat subscription.
"""

from datetime import datetime

from pydantic import ConfigDict

from linten.types.llms.base import LintenPydanticObjectBase


class Linten_SubscriptionAccountTable(LintenPydanticObjectBase):
    model_config = ConfigDict(protected_namespaces=(), frozen=True)

    subscription_account_id: str
    custom_llm_provider: str
    account_id: str
    label: str | None = None
    monthly_fee: float
    currency: str
    billing_period_start: str
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
