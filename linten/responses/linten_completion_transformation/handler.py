"""
Handler for transforming responses api requests to linten.completion requests
"""

from collections.abc import Coroutine, Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from pydantic import TypeAdapter

import linten
from linten.linten_core_utils.allowed_tools_tool_choice import unenforced_allowed_tools_tool_choice
from linten.linten_core_utils.core_helpers import drops_unsupported_params
from linten.linten_core_utils.model_param_helper import embeds_thought_signature_in_tool_call_id
from linten.responses.additional_tools import HoistedAdditionalTools, hoist_additional_tools
from linten.responses.linten_completion_transformation.client_tool_search import bridge_client_tool_search
from linten.responses.linten_completion_transformation.compaction_items import holds_compaction_summary
from linten.responses.linten_completion_transformation.session_handler import ResponsesSessionHandler, StoredTurns
from linten.responses.linten_completion_transformation.streaming_iterator import (
    LintenCompletionStreamingIterator,
)
from linten.responses.linten_completion_transformation.tool_search import has_client_tool_search
from linten.responses.linten_completion_transformation.transformation import (
    LintenCompletionResponsesConfig,
    with_compaction_items_as_params,
)
from linten.responses.streaming_iterator import BaseResponsesAPIStreamingIterator
from linten.types.llms.openai import (
    ResponseInputParam,
    ResponsesAPIOptionalRequestParams,
    ResponsesAPIResponse,
)
from linten.types.utils import ModelResponse

_REQUEST_KWARGS_ADAPTER: Final = TypeAdapter(dict[str, object])
_BRIDGE_TRANSFORM_KEYWORDS: Final = frozenset({"caller_input", "names_non_string_fields"})


def _without_bridge_transform_keywords(request_kwargs: Mapping[str, object]) -> Mapping[str, object]:
    return MappingProxyType(
        {key: value for key, value in request_kwargs.items() if key not in _BRIDGE_TRANSFORM_KEYWORDS}
    )


def _chat_verbosity(responses_api_request: Mapping[str, object]) -> Mapping[str, object]:
    match responses_api_request.get("text"):
        case {"verbosity": str() as verbosity}:
            return {"verbosity": verbosity}
        case _:
            return {}


@dataclass(frozen=True, slots=True)
class _BridgedRequest:
    input: str | ResponseInputParam
    responses_api_request: ResponsesAPIOptionalRequestParams


def _bridged_request(
    hoisted: HoistedAdditionalTools,
    responses_api_request: ResponsesAPIOptionalRequestParams,
    loaded_earlier: Sequence[Mapping[str, object]],
) -> _BridgedRequest:
    searched: Final = bridge_client_tool_search(hoisted.input, hoisted.tools, loaded_earlier)
    return _BridgedRequest(
        input=searched.input,
        responses_api_request=(
            {**responses_api_request, "tools": list(searched.tools)}
            if hoisted.hoisted or searched.bridged
            else responses_api_request
        ),
    )


def _with_the_tool_choice_sent(
    responses_api_request: ResponsesAPIOptionalRequestParams,
    custom_llm_provider: str | None,
    request_kwargs: Mapping[str, object],
) -> ResponsesAPIOptionalRequestParams:
    api_version: Final = request_kwargs.get("api_version")
    tool_choice: Final[object] = responses_api_request.get(  # pyright: ignore[reportUnknownMemberType]  # ToolChoice has an untyped member
        "tool_choice"
    )
    if not unenforced_allowed_tools_tool_choice(
        tool_choice, custom_llm_provider, api_version if isinstance(api_version, str) else None
    ):
        return responses_api_request
    return {**responses_api_request, "tool_choice": None}


class LintenCompletionTransformationHandler:
    def response_api_handler(
        self,
        previous_response_client_ids: tuple[str, ...] = (),
        /,
        *,
        model: str,
        input: str | ResponseInputParam,
        responses_api_request: ResponsesAPIOptionalRequestParams,
        custom_llm_provider: str | None = None,
        _is_async: bool = False,
        stream: bool | None = None,
        extra_headers: Mapping[str, object] | None = None,
        **kwargs,
    ) -> (
        ResponsesAPIResponse
        | BaseResponsesAPIStreamingIterator
        | Coroutine[object, object, ResponsesAPIResponse | BaseResponsesAPIStreamingIterator]
    ):
        hoisted: Final = hoist_additional_tools(
            input,
            responses_api_request.get("tools"),
            drop_params=drops_unsupported_params(_REQUEST_KWARGS_ADAPTER.validate_python(kwargs).get("drop_params")),
        )
        previous_response_id: Final = responses_api_request.get("previous_response_id")
        if _is_async and previous_response_id and has_client_tool_search(hoisted.tools):
            return self._async_response_api_handler_after_earlier_searches(
                previous_response_client_ids,
                previous_response_id,
                hoisted,
                model=model,
                caller_input=input,
                responses_api_request=responses_api_request,
                custom_llm_provider=custom_llm_provider,
                stream=stream,
                extra_headers=extra_headers,
                request_kwargs=_REQUEST_KWARGS_ADAPTER.validate_python(kwargs),
            )
        bridged: Final = _bridged_request(hoisted, responses_api_request, ())
        bridged_input: Final = bridged.input
        bridged_request: Final = bridged.responses_api_request
        linten_completion_request: Final[dict] = {
            **LintenCompletionResponsesConfig.transform_responses_api_request_to_chat_completion_request(
                model=model,
                input=bridged_input,
                caller_input=input,
                names_non_string_fields=True,
                responses_api_request=bridged_request,
                custom_llm_provider=custom_llm_provider,
                stream=stream,
                extra_headers=extra_headers,
                **_without_bridge_transform_keywords(_REQUEST_KWARGS_ADAPTER.validate_python(kwargs)),
            ),
            **_chat_verbosity(bridged_request),
        }
        echoed_request: Final = _with_the_tool_choice_sent(
            bridged_request, custom_llm_provider, _REQUEST_KWARGS_ADAPTER.validate_python(kwargs)
        )

        if _is_async:
            return self.async_response_api_handler(
                previous_response_client_ids,
                linten_completion_request=linten_completion_request,
                request_input=bridged_input,
                responses_api_request=echoed_request,
                **kwargs,
            )

        linten_completion_response: Final[ModelResponse | linten.CustomStreamWrapper] = linten.completion(
            **{**kwargs, **linten_completion_request, "_skip_responses_api_bridge": True},
        )

        if isinstance(linten_completion_response, ModelResponse):
            responses_api_response: Final[ResponsesAPIResponse] = (
                LintenCompletionResponsesConfig.transform_chat_completion_response_to_responses_api_response(
                    chat_completion_response=linten_completion_response,
                    request_input=bridged_input,
                    responses_api_request=echoed_request,
                )
            )

            return responses_api_response

        elif isinstance(linten_completion_response, linten.CustomStreamWrapper):
            return LintenCompletionStreamingIterator(
                model=model,
                linten_custom_stream_wrapper=linten_completion_response,
                request_input=bridged_input,
                responses_api_request=echoed_request,
                custom_llm_provider=custom_llm_provider,
                linten_metadata=kwargs.get("linten_metadata", {}),
                tool_call_provider_fields=not embeds_thought_signature_in_tool_call_id(
                    _REQUEST_KWARGS_ADAPTER.validate_python(kwargs)
                ),
            )
        raise ValueError(f"Unexpected response type: {type(linten_completion_response)}")

    async def _async_response_api_handler_after_earlier_searches(
        self,
        previous_response_client_ids: tuple[str, ...],
        previous_response_id: str,
        hoisted: HoistedAdditionalTools,
        /,
        *,
        model: str,
        caller_input: str | ResponseInputParam,
        responses_api_request: ResponsesAPIOptionalRequestParams,
        custom_llm_provider: str | None,
        stream: bool | None,
        extra_headers: Mapping[str, object] | None,
        request_kwargs: Mapping[str, object],
    ) -> ResponsesAPIResponse | BaseResponsesAPIStreamingIterator:
        stored_turns: Final = await ResponsesSessionHandler.get_stored_turns_for_previous_response_id(
            previous_response_id, previous_response_client_ids
        )
        bridged: Final = _bridged_request(
            hoisted,
            responses_api_request,
            ResponsesSessionHandler.client_tool_search_tools_loaded_before(
                stored_turns, previous_response_id, previous_response_client_ids
            ),
        )
        return await self.async_response_api_handler(
            previous_response_client_ids,
            stored_turns,
            linten_completion_request={
                **LintenCompletionResponsesConfig.transform_responses_api_request_to_chat_completion_request(
                    model=model,
                    input=bridged.input,
                    caller_input=caller_input,
                    names_non_string_fields=True,
                    responses_api_request=bridged.responses_api_request,
                    custom_llm_provider=custom_llm_provider,
                    stream=stream,
                    extra_headers=extra_headers,
                    **_without_bridge_transform_keywords(request_kwargs),
                ),
                **_chat_verbosity(bridged.responses_api_request),
            },
            request_input=bridged.input,
            responses_api_request=_with_the_tool_choice_sent(
                bridged.responses_api_request, custom_llm_provider, request_kwargs
            ),
            **request_kwargs,
        )

    async def async_response_api_handler(
        self,
        previous_response_client_ids: tuple[str, ...] = (),
        stored_turns: StoredTurns | None = None,
        /,
        *,
        linten_completion_request: dict,
        request_input: str | ResponseInputParam,
        responses_api_request: ResponsesAPIOptionalRequestParams,
        **kwargs,
    ) -> ResponsesAPIResponse | BaseResponsesAPIStreamingIterator:
        previous_response_id: Final[str | None] = responses_api_request.get("previous_response_id")
        if previous_response_id:
            linten_completion_request = await LintenCompletionResponsesConfig.async_responses_api_session_handler(
                previous_response_id=previous_response_id,
                linten_completion_request=linten_completion_request,
                instructions=responses_api_request.get("instructions"),
                request_kwargs=_REQUEST_KWARGS_ADAPTER.validate_python(kwargs),
                previous_response_client_ids=previous_response_client_ids,
                stored_turns=stored_turns,
                input_replaces_history=holds_compaction_summary(with_compaction_items_as_params(request_input)),
            )

        linten_completion_response: Final[ModelResponse | linten.CustomStreamWrapper] = await linten.acompletion(
            **{**kwargs, **linten_completion_request, "_skip_responses_api_bridge": True},
        )
        if isinstance(linten_completion_response, ModelResponse):
            responses_api_response: Final[ResponsesAPIResponse] = (
                LintenCompletionResponsesConfig.transform_chat_completion_response_to_responses_api_response(
                    chat_completion_response=linten_completion_response,
                    request_input=request_input,
                    responses_api_request=responses_api_request,
                )
            )

            return responses_api_response

        elif isinstance(linten_completion_response, linten.CustomStreamWrapper):
            return LintenCompletionStreamingIterator(
                model=linten_completion_request.get("model") or "",
                linten_custom_stream_wrapper=linten_completion_response,
                request_input=request_input,
                responses_api_request=responses_api_request,
                custom_llm_provider=linten_completion_request.get("custom_llm_provider"),
                linten_metadata=kwargs.get("linten_metadata", {}),
                tool_call_provider_fields=not embeds_thought_signature_in_tool_call_id(
                    _REQUEST_KWARGS_ADAPTER.validate_python(kwargs)
                ),
            )
        raise ValueError(f"Unexpected response type: {type(linten_completion_response)}")
