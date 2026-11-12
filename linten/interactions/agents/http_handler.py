"""
HTTP handler for the Agents API.

Extends InteractionsHTTPHandler so that the shared HTTP infrastructure
(_handle_error, _sync_client, _async_client) is reused rather than
duplicated. BaseAgentsAPIConfig stays as pure transform code.
"""

from collections.abc import Coroutine, Mapping
from typing import Final

import httpx

from linten.constants import request_timeout
from linten.interactions.http_handler import InteractionsHTTPHandler
from linten.linten_core_utils.linten_logging import Logging as LintenLoggingObj
from linten.llms.base_llm.agents.transformation import BaseAgentsAPIConfig
from linten.llms.custom_httpx.http_handler import AsyncHTTPHandler, HTTPHandler
from linten.types.agents import (
    AgentCreateRequest,
    AgentCreateResponse,
    AgentDeleteResult,
    AgentListResponse,
    AgentVersionsResponse,
)
from linten.types.router import GenericLintenParams


class AgentsHTTPHandler(InteractionsHTTPHandler):
    """HTTP handler for Agents API CRUD requests."""

    # ------------------------------------------------------------------ #
    # CREATE                                                               #
    # ------------------------------------------------------------------ #

    def create_agent(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        create_request: AgentCreateRequest,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        extra_body: Mapping[str, object] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: HTTPHandler | None = None,
        _is_async: bool = False,
    ) -> AgentCreateResponse | Coroutine[object, object, AgentCreateResponse]:
        if _is_async:
            return self.async_create_agent(
                agents_api_config=agents_api_config,
                create_request=create_request,
                linten_params=linten_params,
                logging_obj=logging_obj,
                extra_headers=extra_headers,
                extra_body=extra_body,
                timeout=timeout,
            )

        sync_httpx_client: Final = self._sync_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url: Final = agents_api_config.get_complete_url(
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        data: Final = {
            **agents_api_config.transform_create_request(create_request),
            **(extra_body or {}),
        }

        logging_obj.pre_call(
            input=create_request.id,
            api_key="",
            additional_args={
                "complete_input_dict": data,
                "api_base": url,
                "headers": headers,
            },
        )
        try:
            response = sync_httpx_client.post(url=url, headers=headers, json=data, timeout=timeout or request_timeout)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(
            original_response=response.text,
            additional_args={"complete_input_dict": data},
        )
        return agents_api_config.transform_create_response(raw_response=response, name=create_request.id)

    async def async_create_agent(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        create_request: AgentCreateRequest,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        extra_body: Mapping[str, object] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: AsyncHTTPHandler | None = None,
    ) -> AgentCreateResponse:
        async_httpx_client: Final = self._async_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url: Final = agents_api_config.get_complete_url(
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        data: Final = {
            **agents_api_config.transform_create_request(create_request),
            **(extra_body or {}),
        }

        logging_obj.pre_call(
            input=create_request.id,
            api_key="",
            additional_args={
                "complete_input_dict": data,
                "api_base": url,
                "headers": headers,
            },
        )
        try:
            response: Final = await async_httpx_client.post(
                url=url, headers=headers, json=data, timeout=timeout or request_timeout
            )
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(
            original_response=response.text,
            additional_args={"complete_input_dict": data},
        )
        return agents_api_config.transform_create_response(raw_response=response, name=create_request.id)

    # ------------------------------------------------------------------ #
    # LIST                                                                 #
    # ------------------------------------------------------------------ #

    def list_agents(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: HTTPHandler | None = None,
        _is_async: bool = False,
    ) -> AgentListResponse | Coroutine[object, object, AgentListResponse]:
        if _is_async:
            return self.async_list_agents(
                agents_api_config=agents_api_config,
                linten_params=linten_params,
                logging_obj=logging_obj,
                extra_headers=extra_headers,
                timeout=timeout,
            )

        sync_httpx_client: Final = self._sync_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url, params = agents_api_config.transform_list_request(
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input="list_agents",
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response: Final = sync_httpx_client.get(url=url, headers=headers, params=params)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_list_response(raw_response=response)

    async def async_list_agents(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: AsyncHTTPHandler | None = None,
    ) -> AgentListResponse:
        async_httpx_client: Final = self._async_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url, params = agents_api_config.transform_list_request(
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input="list_agents",
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response: Final = await async_httpx_client.get(url=url, headers=headers, params=params)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_list_response(raw_response=response)

    # ------------------------------------------------------------------ #
    # GET                                                                  #
    # ------------------------------------------------------------------ #

    def get_agent(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        name: str,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: HTTPHandler | None = None,
        _is_async: bool = False,
    ) -> AgentCreateResponse | Coroutine[object, object, AgentCreateResponse]:
        if _is_async:
            return self.async_get_agent(
                agents_api_config=agents_api_config,
                name=name,
                linten_params=linten_params,
                logging_obj=logging_obj,
                extra_headers=extra_headers,
                timeout=timeout,
            )

        sync_httpx_client: Final = self._sync_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url, params = agents_api_config.transform_get_request(
            name=name,
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input=name,
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response: Final = sync_httpx_client.get(url=url, headers=headers, params=params)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_get_response(raw_response=response, name=name)

    async def async_get_agent(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        name: str,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: AsyncHTTPHandler | None = None,
    ) -> AgentCreateResponse:
        async_httpx_client: Final = self._async_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url, params = agents_api_config.transform_get_request(
            name=name,
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input=name,
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response: Final = await async_httpx_client.get(url=url, headers=headers, params=params)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_get_response(raw_response=response, name=name)

    # ------------------------------------------------------------------ #
    # DELETE                                                               #
    # ------------------------------------------------------------------ #

    def delete_agent(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        name: str,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: HTTPHandler | None = None,
        _is_async: bool = False,
    ) -> AgentDeleteResult | Coroutine[object, object, AgentDeleteResult]:
        if _is_async:
            return self.async_delete_agent(
                agents_api_config=agents_api_config,
                name=name,
                linten_params=linten_params,
                logging_obj=logging_obj,
                extra_headers=extra_headers,
                timeout=timeout,
            )

        sync_httpx_client: Final = self._sync_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url: Final = agents_api_config.transform_delete_request(
            name=name,
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input=name,
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response: Final = sync_httpx_client.delete(url=url, headers=headers, timeout=timeout or request_timeout)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_delete_response(raw_response=response, name=name)

    async def async_delete_agent(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        name: str,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: AsyncHTTPHandler | None = None,
    ) -> AgentDeleteResult:
        async_httpx_client: Final = self._async_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url: Final = agents_api_config.transform_delete_request(
            name=name,
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input=name,
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response = await async_httpx_client.delete(url=url, headers=headers, timeout=timeout or request_timeout)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_delete_response(raw_response=response, name=name)

    # ------------------------------------------------------------------ #
    # LIST VERSIONS                                                        #
    # ------------------------------------------------------------------ #

    def list_agent_versions(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        name: str,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: HTTPHandler | None = None,
        _is_async: bool = False,
    ) -> AgentVersionsResponse | Coroutine[object, object, AgentVersionsResponse]:
        if _is_async:
            return self.async_list_agent_versions(
                agents_api_config=agents_api_config,
                name=name,
                linten_params=linten_params,
                logging_obj=logging_obj,
                extra_headers=extra_headers,
                timeout=timeout,
            )

        sync_httpx_client: Final = self._sync_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url, params = agents_api_config.transform_list_versions_request(
            name=name,
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input=name,
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response: Final = sync_httpx_client.get(url=url, headers=headers, params=params)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_list_versions_response(raw_response=response, name=name)

    async def async_list_agent_versions(
        self,
        agents_api_config: BaseAgentsAPIConfig,
        name: str,
        linten_params: GenericLintenParams,
        logging_obj: LintenLoggingObj,
        extra_headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: AsyncHTTPHandler | None = None,
    ) -> AgentVersionsResponse:
        async_httpx_client: Final = self._async_client(linten_params, client)
        headers: Final = agents_api_config.validate_environment(
            headers=extra_headers or {}, linten_params=dict(linten_params)
        )
        url, params = agents_api_config.transform_list_versions_request(
            name=name,
            api_base=linten_params.get("api_base"),
            linten_params=dict(linten_params),
        )
        logging_obj.pre_call(
            input=name,
            api_key="",
            additional_args={"api_base": url, "headers": headers},
        )
        try:
            response: Final = await async_httpx_client.get(url=url, headers=headers, params=params)
        except Exception as e:
            raise self._handle_error(e=e, provider_config=agents_api_config)

        logging_obj.post_call(original_response=response.text, additional_args={})
        return agents_api_config.transform_list_versions_response(raw_response=response, name=name)


agents_http_handler: Final = AgentsHTTPHandler()
