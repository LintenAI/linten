from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from linten.types.llms.base import LintenBaseModel

T = TypeVar("T", bound=BaseModel)


class GuardrailConfigModel(LintenBaseModel, Generic[T], ABC):
    """Base model for guardrail configuration"""

    optional_params: T | None = Field(
        default=None,
        description="Optional parameters for the guardrail",
    )

    @staticmethod
    @abstractmethod
    def ui_friendly_name() -> str:
        """UI-friendly name for the guardrail"""
