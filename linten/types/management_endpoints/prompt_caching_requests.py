from datetime import datetime
from typing import Literal, TypeAlias

from pydantic import ConfigDict

from linten.types.llms.base import LintenBaseModel

PromptCachingRequestFilter: TypeAlias = Literal["all", "injected", "hits"]


class PromptCachingRequest(LintenBaseModel):
    model_config = ConfigDict(frozen=True)

    request_id: str
    start_time: datetime
    model: str
    gateway_injected: bool
    cache_read_tokens: int
    cache_creation_tokens: int
    spend: float
    net_savings: float | None


class PromptCachingRequestCursor(LintenBaseModel):
    model_config = ConfigDict(frozen=True)

    start_time: datetime
    request_id: str


class PromptCachingRequestsResponse(LintenBaseModel):
    model_config = ConfigDict(frozen=True)

    requests: tuple[PromptCachingRequest, ...]
    page_size: int
    has_more: bool
    next_cursor: PromptCachingRequestCursor | None
