from typing import Final

from linten.linten_core_utils.resource_ownership import (
    get_primary_resource_owner_scope,
    get_resource_owner_scopes,
    is_proxy_admin,
    user_can_access_resource_owner,
)
from linten.types.proxy.auth.user_api_key_auth import UserAPIKeyAuth
from linten.types.proxy.auth.user_roles import LintenUserRoles

__all__ = [
    "Final",
    "LintenUserRoles",
    "UserAPIKeyAuth",
    "get_primary_resource_owner_scope",
    "get_resource_owner_scopes",
    "is_proxy_admin",
    "user_can_access_resource_owner",
]
