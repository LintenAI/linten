from pydantic import BaseModel, ConfigDict

from linten.proxy._types import LintenUserRoles


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_id: str
    user_role: LintenUserRoles | None
    user_email: str | None
