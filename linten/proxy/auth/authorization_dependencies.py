from __future__ import annotations

from collections.abc import Awaitable, Callable
from functools import partial
from typing import TYPE_CHECKING, Annotated, Final, TypeAlias

from fastapi import Depends

from linten.proxy._types import Linten_TeamTable, UserAPIKeyAuth
from linten.proxy.auth.authorization import permitted_log_team_ids

if TYPE_CHECKING:
    from linten.proxy.common_utils.user_api_key_cache import UserApiKeyCache
    from linten.proxy.utils import PrismaClient, ProxyLogging


LogTeamLookup: TypeAlias = Callable[[UserAPIKeyAuth], Awaitable[tuple[str, ...]]]


async def load_permitted_log_team_ids(
    auth: UserAPIKeyAuth,
    *,
    prisma_client: PrismaClient | None,
    user_api_key_cache: UserApiKeyCache,
    proxy_logging_obj: ProxyLogging,
) -> tuple[str, ...]:
    from linten.proxy.auth.auth_checks import get_user_object
    from linten.repositories.team_repository import TeamRepository

    if prisma_client is None:
        return ()
    user_obj: Final = await get_user_object(
        user_id=auth.user_id,
        prisma_client=prisma_client,
        user_api_key_cache=user_api_key_cache,
        user_id_upsert=False,
        proxy_logging_obj=proxy_logging_obj,
    )
    if user_obj is None or not user_obj.teams:
        return ()
    team_rows: Final = await TeamRepository(prisma_client).table.find_many(where={"team_id": {"in": user_obj.teams}})
    return permitted_log_team_ids(auth, (Linten_TeamTable.model_validate(row.model_dump()) for row in team_rows))


async def get_log_team_lookup() -> LogTeamLookup:
    """Bind infrastructure without performing permission I/O before the handler's checks."""
    from linten.proxy.proxy_server import prisma_client, proxy_logging_obj, user_api_key_cache

    return partial(
        load_permitted_log_team_ids,
        prisma_client=prisma_client,
        user_api_key_cache=user_api_key_cache,
        proxy_logging_obj=proxy_logging_obj,
    )


LogTeamLookupDependency: TypeAlias = Annotated[LogTeamLookup, Depends(get_log_team_lookup)]
