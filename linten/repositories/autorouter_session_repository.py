"""
Repository for the auto-router per-session rollup (Linten_AutoRouterSession).
"""

from typing import TYPE_CHECKING, Final

from linten.models.autorouter_session import Linten_AutoRouterSession
from linten.repositories.base_repository import BaseRepository
from linten.repositories.prisma_protocols import TableActions
from linten.repositories.table_repositories import PrismaTableRepository

if TYPE_CHECKING:
    from prisma import models as prisma_models


class _AutoRouterSessionTable(PrismaTableRepository["prisma_models.Linten_AutoRouterSession"]):
    table_name = "linten_autoroutersession"


class AutoRouterSessionRepository(BaseRepository[Linten_AutoRouterSession]):
    @property
    def table(self) -> TableActions["prisma_models.Linten_AutoRouterSession"]:
        return _AutoRouterSessionTable(self._prisma_client).table

    @property
    def model_class(self) -> type[Linten_AutoRouterSession]:
        return Linten_AutoRouterSession

    async def find_latest_for_key(self, api_key: str, session_id: str) -> Linten_AutoRouterSession | None:
        """The session's most recently active router row under exactly this key hash, or None.

        The key is the row's own partition, not a filter over a wider read: the spend writer keyed the
        row under the caller's api_key, so a key can only ever see what it wrote itself.
        """
        record: Final = await self.table.find_first(
            where={"api_key": api_key, "session_id": session_id},
            order={"last_turn_at": "desc"},
        )
        return self._to_model(record)
