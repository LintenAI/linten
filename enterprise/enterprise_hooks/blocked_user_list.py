# +------------------------------+
#
#        Blocked User List
#
# +------------------------------+
#  Thank you users! We ❤️ you! - Krrish & Ishaan
## This accepts a list of user id's for whom calls will be rejected


from typing import Final, Literal, Optional

from fastapi import HTTPException
from pydantic import TypeAdapter

import linten
from linten._internal_context import with_service_target
from linten._logging import verbose_proxy_logger
from linten.caching.caching import DualCache
from linten.integrations.custom_logger import CustomLogger
from linten.proxy._types import Linten_EndUserTable, UserAPIKeyAuth
from linten.proxy.common_utils.user_api_key_cache import AUTH_OBJECTS_TARGET
from linten.proxy.utils import PrismaClient
from linten.repositories.table_repositories import EndUserRepository

_REQUEST_BODY_VALUE: Final = TypeAdapter(object)


class ENTERPRISE_BlockedUserList(CustomLogger):
    enforces_request_content: bool = True
    # Class variables or attributes
    def __init__(self, prisma_client: Optional[PrismaClient]):
        self.prisma_client = prisma_client

        blocked_user_list = linten.blocked_user_list
        if blocked_user_list is None:
            self.blocked_user_list = None
            return

        if isinstance(blocked_user_list, list):
            self.blocked_user_list = blocked_user_list

        if isinstance(blocked_user_list, str):  # assume it's a filepath
            try:
                with open(blocked_user_list, "r") as file:
                    data = file.read()
                    self.blocked_user_list = data.split("\n")
            except FileNotFoundError:
                raise Exception(
                    f"File not found. blocked_user_list={blocked_user_list}"
                )
            except Exception as e:
                raise Exception(
                    f"An error occurred: {str(e)}, blocked_user_list={blocked_user_list}"
                )

    def print_verbose(self, print_statement, level: Literal["INFO", "DEBUG"] = "DEBUG"):
        if level == "INFO":
            verbose_proxy_logger.info(print_statement)
        elif level == "DEBUG":
            verbose_proxy_logger.debug(print_statement)

        if linten.set_verbose is True:
            print(print_statement)  # noqa

    @with_service_target(AUTH_OBJECTS_TARGET)
    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: str,
    ):
        try:
            """
            - check if user id part of call
            - check if user id part of blocked list
                - if blocked list is none or user not in blocked list
                - check if end-user in cache
                - check if end-user in db
            """
            self.print_verbose("Inside Blocked User List Pre-Call Hook")
            if "user_id" in data or "user" in data:
                user = data.get("user_id", data.get("user", ""))
                if (
                    self.blocked_user_list is not None
                    and user in self.blocked_user_list
                ):
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "error": f"User blocked from making LLM API Calls. User={user}"
                        },
                    )

                cache_key = f"linten:end_user_id:{user}"
                end_user_cache_obj: Optional[Linten_EndUserTable] = cache.get_cache(  # type: ignore
                    key=cache_key
                )
                if end_user_cache_obj is None and self.prisma_client is not None:
                    # check db
                    end_user_id: Final = _REQUEST_BODY_VALUE.validate_python(user)
                    end_user_obj = await EndUserRepository(
                        self.prisma_client
                    ).table.find_unique(where={"user_id": end_user_id})
                    if end_user_obj is None:  # user not in db - assume not blocked
                        end_user_obj = Linten_EndUserTable(user_id=user, blocked=False)
                    cache.set_cache(key=cache_key, value=end_user_obj, ttl=60)
                    if end_user_obj.blocked is True:
                        raise HTTPException(
                            status_code=400,
                            detail={
                                "error": f"User blocked from making LLM API Calls. User={user}"
                            },
                        )
                elif (
                    end_user_cache_obj is not None
                    and end_user_cache_obj.blocked is True
                ):
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "error": f"User blocked from making LLM API Calls. User={user}"
                        },
                    )

        except HTTPException as e:
            raise e
        except Exception as e:
            verbose_proxy_logger.exception(
                "linten.enterprise.enterprise_hooks.blocked_user_list::async_pre_call_hook - Exception occurred - {}".format(
                    str(e)
                )
            )
_ENTERPRISE_BlockedUserList = ENTERPRISE_BlockedUserList
