from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

import linten
from linten import aresponses
from linten._uuid import uuid
from linten.caching.caching_handler import LLMCachingHandler
from linten.linten_core_utils.linten_logging import Logging as LintenLogging
from linten.types.llms import openai as openai_types
from linten.types.utils import CallTypes


@pytest.mark.asyncio
async def test_async_get_cache_reuses_preset_cache_key_for_responses():
    caching_handler = LLMCachingHandler(
        original_function=aresponses,
        request_kwargs={},
        start_time=datetime.now(),
    )
    logging_obj = LintenLogging(
        linten_call_id=str(datetime.now()),
        call_type=CallTypes.aresponses.value,
        model="gpt-4.1-mini",
        messages=[],
        function_id=str(uuid.uuid4()),
        stream=True,
        start_time=datetime.now(),
    )

    original_cache = linten.cache
    mock_cache = MagicMock()
    mock_cache.supported_call_types = [CallTypes.aresponses.value]
    mock_cache.supports_async.return_value = True
    mock_cache.get_cache_key.return_value = "responses-stream-cache-key"
    mock_cache.async_get_cache = AsyncMock(return_value=None)
    linten.cache = mock_cache

    kwargs = {
        "model": "gpt-4.1-mini",
        "input": "hello",
        "stream": True,
        "linten_params": {},
    }
    await caching_handler.async_get_cache(
        model="gpt-4.1-mini",
        original_function=aresponses,
        logging_obj=logging_obj,
        start_time=datetime.now(),
        call_type=CallTypes.aresponses.value,
        kwargs=kwargs,
    )

    assert caching_handler.preset_cache_key == "responses-stream-cache-key"
    mock_cache.async_get_cache.assert_awaited_once()
    assert (
        mock_cache.async_get_cache.call_args.kwargs["cache_key"]
        == "responses-stream-cache-key"
    )

    linten.cache = original_cache


@pytest.mark.asyncio
async def test_async_get_cache_falls_back_to_sync_cache_for_responses():
    caching_handler = LLMCachingHandler(
        original_function=aresponses,
        request_kwargs={},
        start_time=datetime.now(),
    )
    logging_obj = LintenLogging(
        linten_call_id=str(datetime.now()),
        call_type=CallTypes.aresponses.value,
        model="gpt-4.1-mini",
        messages=[],
        function_id=str(uuid.uuid4()),
        stream=True,
        start_time=datetime.now(),
    )

    original_cache = linten.cache
    mock_cache = MagicMock()
    mock_cache.supported_call_types = [CallTypes.aresponses.value]
    mock_cache.supports_async.return_value = False
    mock_cache.get_cache_key.return_value = "responses-stream-cache-key"
    mock_cache.get_cache.return_value = None
    linten.cache = mock_cache

    kwargs = {
        "model": "gpt-4.1-mini",
        "input": "hello",
        "stream": True,
        "linten_params": {},
    }
    await caching_handler.async_get_cache(
        model="gpt-4.1-mini",
        original_function=aresponses,
        logging_obj=logging_obj,
        start_time=datetime.now(),
        call_type=CallTypes.aresponses.value,
        kwargs=kwargs,
    )

    assert caching_handler.preset_cache_key == "responses-stream-cache-key"
    mock_cache.get_cache.assert_called_once()
    assert mock_cache.get_cache.call_args.kwargs["cache_key"] == (
        "responses-stream-cache-key"
    )

    linten.cache = original_cache


def test_reasoning_summary_events_default_summary_index():
    delta_event = openai_types.ReasoningSummaryTextDeltaEvent(
        type=openai_types.ResponsesAPIStreamEvents.REASONING_SUMMARY_TEXT_DELTA,
        item_id="rs_1",
        output_index=0,
        delta="abc",
    )
    text_done_event = openai_types.ReasoningSummaryTextDoneEvent(
        type=openai_types.ResponsesAPIStreamEvents.REASONING_SUMMARY_TEXT_DONE,
        item_id="rs_1",
        output_index=0,
        sequence_number=1,
        text="abc",
    )
    part_done_event = openai_types.ReasoningSummaryPartDoneEvent(
        type=openai_types.ResponsesAPIStreamEvents.REASONING_SUMMARY_PART_DONE,
        item_id="rs_1",
        output_index=0,
        sequence_number=2,
        part=openai_types.BaseLintenOpenAIResponseObject(
            type="summary_text",
            text="abc",
        ),
    )

    assert delta_event.summary_index == 0
    assert text_done_event.summary_index == 0
    assert part_done_event.summary_index == 0
