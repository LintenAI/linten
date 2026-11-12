from typing import Annotated, Final

from fastapi import APIRouter, Depends

from linten.proxy._types import UserAPIKeyAuth
from linten.proxy.auth.user_api_key_auth import user_api_key_auth
from linten.proxy.management.users.exceptions import current_user_not_found
from linten.proxy.management.users.schemas import CurrentUserResponse
from linten.proxy.management_endpoints.management_v1.common import MANAGEMENT_V1_PREFIX

router: Final = APIRouter(prefix=MANAGEMENT_V1_PREFIX)


@router.get("/users/me", include_in_schema=False)
async def get_current_user(
    caller: Annotated[UserAPIKeyAuth, Depends(user_api_key_auth)],
) -> CurrentUserResponse:
    if caller.user_id is None:
        raise current_user_not_found()
    return CurrentUserResponse(user_id=caller.user_id, user_role=caller.user_role, user_email=caller.user_email)
