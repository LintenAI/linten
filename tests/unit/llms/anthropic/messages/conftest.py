from dataclasses import dataclass
from typing import Final
from unittest.mock import MagicMock

import pytest

from linten.redis.stores.connection import connect
from linten.redis.stores.spend_counters import SpendCounterStore
from pydantic import BaseModel

import linten.proxy.proxy_server as proxy_server
from linten.caching.dual_cache import DualCache
from linten.proxy._types import (
    Linten_EndUserTable,
    Linten_ProjectTableCachedObj,
    Linten_TeamMembership,
    Linten_TeamTableCachedObj,
    Linten_UserTable,
)
from linten.proxy.common_utils.user_api_key_cache import (
    UserApiKeyCache,
    end_user_cache_key,
    project_cache_key,
    team_membership_reservation_cache_key,
)
from linten.proxy.utils import ProxyLogging
from linten.router import Router

_ProxyObject = (
    Linten_TeamTableCachedObj
    | Linten_UserTable
    | Linten_EndUserTable
    | Linten_ProjectTableCachedObj
    | Linten_TeamMembership
)


def _cache_key(row: _ProxyObject) -> str:
    match row:
        case Linten_TeamTableCachedObj():
            return f"team_id:{row.team_id}"
        case Linten_UserTable():
            return row.user_id
        case Linten_EndUserTable():
            return end_user_cache_key(row.user_id)
        case Linten_ProjectTableCachedObj():
            return project_cache_key(row.project_id)
        case Linten_TeamMembership():
            return team_membership_reservation_cache_key(user_id=row.user_id, team_id=row.team_id)


@dataclass(frozen=True, slots=True)
class ProxyAuthState:
    """A running proxy with a master key, so the centralized auth checks run, and its auth cache to seed."""

    cache: UserApiKeyCache
    monkeypatch: pytest.MonkeyPatch

    def seed(self, *rows: _ProxyObject) -> None:
        for row in rows:
            stored: Final[BaseModel] = row
            self.cache.set_cache(key=_cache_key(row), value=stored)

    def serve(self, router: Router) -> None:
        self.monkeypatch.setattr(proxy_server, "llm_router", router)


@pytest.fixture
def proxy_auth_state(monkeypatch: pytest.MonkeyPatch) -> ProxyAuthState:
    cache: Final = UserApiKeyCache()
    proxy_globals: Final = {
        "master_key": "sk-test-master",
        "prisma_client": MagicMock(),
        "user_api_key_cache": cache,
        "spend_counter_cache": DualCache(),
        "spend_counter_store": SpendCounterStore(connect(None).spend_counters()),
        "proxy_logging_obj": ProxyLogging(user_api_key_cache=cache),
        "general_settings": {},
        "user_custom_auth": None,
        "linten_proxy_admin_name": "admin",
        "llm_router": None,
        "llm_model_list": None,
    }
    for name, value in proxy_globals.items():
        monkeypatch.setattr(proxy_server, name, value)
    return ProxyAuthState(cache=cache, monkeypatch=monkeypatch)
