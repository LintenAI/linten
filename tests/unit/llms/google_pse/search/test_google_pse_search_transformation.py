import datetime

import httpx
import pytest
from pydantic import ValidationError

from linten.linten_core_utils.linten_logging import Logging
from linten.llms.base_llm.search.transformation import SearchResponse, SearchResult
from linten.llms.google_pse.search.transformation import GooglePSESearchConfig


def _transform(payload: object) -> SearchResponse:
    logging_obj = Logging(
        model="google_pse/search",
        messages=[],
        stream=False,
        call_type="search",
        start_time=datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc),
        linten_call_id="call-id",
        function_id="function-id",
    )
    return GooglePSESearchConfig().transform_search_response(
        raw_response=httpx.Response(200, json=payload), logging_obj=logging_obj
    )


def test_google_pse_items_keep_provider_order_and_ignore_search_metadata():
    response = _transform(
        {
            "kind": "customsearch#search",
            "url": {"type": "application/json", "template": "https://www.googleapis.com/customsearch/v1?q={q}"},
            "queries": {"request": [{"title": "Google Custom Search - linten", "totalResults": "2", "count": 2}]},
            "searchInformation": {"searchTime": 0.21, "formattedSearchTime": "0.21", "totalResults": "2"},
            "items": [
                {
                    "kind": "customsearch#result",
                    "title": "Linten",
                    "htmlTitle": "<b>Linten</b>",
                    "link": "https://example.com/linten",
                    "displayLink": "example.com",
                    "snippet": "Call every LLM API",
                    "htmlSnippet": "Call every <b>LLM</b> API",
                    "pagemap": {"metatags": [{"og:title": "Linten"}]},
                },
                {"title": "Docs", "link": "https://example.com/docs", "snippet": "Docs"},
            ],
        }
    )

    assert response.object == "search"
    assert response.results == [
        SearchResult(title="Linten", url="https://example.com/linten", snippet="Call every LLM API"),
        SearchResult(title="Docs", url="https://example.com/docs", snippet="Docs"),
    ]


def test_google_pse_item_without_title_link_or_snippet_gets_empty_strings():
    assert _transform({"items": [{"kind": "customsearch#result"}]}).results == [
        SearchResult(title="", url="", snippet="", date=None, last_updated=None)
    ]


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"kind": "customsearch#search", "searchInformation": {"totalResults": "0"}},
        {"items": []},
        {"items": ""},
        {"items": {}},
    ],
)
def test_google_pse_response_without_items_is_empty(payload):
    assert _transform(payload).results == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title", None),
        ("title", 7),
        ("link", None),
        ("link", ["https://example.com"]),
        ("snippet", None),
        ("snippet", {"text": "snippet"}),
    ],
)
def test_google_pse_item_with_field_of_wrong_type_is_rejected(field, value):
    item = {"title": "T", "link": "https://example.com", "snippet": "S", field: value}

    with pytest.raises(ValidationError):
        _transform({"items": [item]})


def test_google_pse_item_with_several_fields_of_wrong_type_reports_every_field():
    item = {"title": 7, "link": None, "snippet": ["snippet"]}

    with pytest.raises(ValidationError) as exc_info:
        _transform({"items": [item]})

    assert [error["loc"] for error in exc_info.value.errors()] == [("title",), ("url",), ("snippet",)]


def test_google_pse_malformed_item_is_rejected_without_naming_its_position():
    items = [{}] * 429 + ["not-an-object"]

    with pytest.raises(ValidationError) as exc_info:
        _transform({"items": items})

    assert "429" not in str(exc_info.value)
