import base64
import json
from collections.abc import Mapping, Sequence
from typing import Final

import httpx
import pytest

import linten
from linten.proxy._types import UserAPIKeyAuth
from linten.proxy.vector_store_endpoints.utils import get_linten_managed_vector_store, with_managed_search_file_ids
from linten.types.utils import SpecialEnums
from linten.vector_stores.vector_store_registry import VectorStoreRegistry


def _registered_store(linten_params: object) -> dict[str, object]:
    return {
        "vector_store_id": "vs_1",
        "custom_llm_provider": "bedrock",
        "vector_store_name": "kb",
        "vector_store_metadata": '{"source": "db"}',
        "team_id": None,
        "linten_params": linten_params,
    }


@pytest.mark.parametrize(
    ("stored_params", "expected_params"),
    [
        (
            '{"api_base": "https://example.com", "embedding": {"api_key": "sk-1", "dims": [1, null]}}',
            {"api_base": "https://example.com", "embedding": {"api_key": "sk-1", "dims": [1, None]}},
        ),
        (
            '{"top_k": 12, "score_threshold": 12.0, "api_version": "12", "stream": true, "verify": false,'
            ' "region": null, "max_tokens": 123456789012345678901234567890}',
            {
                "top_k": 12,
                "score_threshold": 12.0,
                "api_version": "12",
                "stream": True,
                "verify": False,
                "region": None,
                "max_tokens": 123456789012345678901234567890,
            },
        ),
        ('{"z": 1, "a": 2, "a": 3}', {"z": 1, "a": 3}),
        ("{}", {}),
    ],
)
async def test_registry_store_with_json_object_string_params_resolves_to_decoded_params(
    monkeypatch: pytest.MonkeyPatch, stored_params: str, expected_params: dict[str, object]
):
    store = _registered_store(stored_params)
    monkeypatch.setattr(linten, "vector_store_registry", VectorStoreRegistry([store]))

    resolved = await get_linten_managed_vector_store("vs_1")

    assert resolved == {**store, "linten_params": expected_params}
    assert json.dumps(resolved["linten_params"]) == json.dumps(expected_params)
    assert store["linten_params"] == stored_params


@pytest.mark.parametrize(
    "stored_params",
    [
        "[1, 2]",
        '[["api_base", "https://example.com"]]',
        '"{\\"api_base\\": \\"https://example.com\\"}"',
        "12",
        "12.5",
        "true",
        "null",
        "{not json",
        "",
    ],
)
async def test_registry_store_with_non_object_or_invalid_json_string_params_resolves_to_empty_params(
    monkeypatch: pytest.MonkeyPatch, stored_params: str
):
    store = _registered_store(stored_params)
    monkeypatch.setattr(linten, "vector_store_registry", VectorStoreRegistry([store]))

    resolved = await get_linten_managed_vector_store("vs_1")

    assert resolved == {**store, "linten_params": {}}
    assert store["linten_params"] == stored_params


@pytest.mark.parametrize("stored_params", [{"api_base": "https://example.com"}, {}, None])
async def test_registry_store_with_non_string_params_is_returned_as_is(
    monkeypatch: pytest.MonkeyPatch, stored_params: object
):
    store = _registered_store(stored_params)
    monkeypatch.setattr(linten, "vector_store_registry", VectorStoreRegistry([store]))

    resolved = await get_linten_managed_vector_store("vs_1")

    assert resolved is store
    assert resolved["linten_params"] is stored_params


def _managed_file_id(provider_file_id: str) -> str:
    unified_file_id: Final = SpecialEnums.LINTEN_MANAGED_FILE_COMPLETE_STR.value.format(
        "text/plain", "unified-1", "openai/team-provider", provider_file_id, "team-deployment"
    )
    return base64.urlsafe_b64encode(unified_file_id.encode()).decode().rstrip("=")


class _ManagedFileIds:
    def __init__(self, unified_file_ids: Mapping[str, str]) -> None:
        self.unified_file_ids: Final = unified_file_ids

    async def get_unified_file_ids_for_provider_file_ids(
        self, provider_file_ids: Sequence[str], user_api_key_dict: UserAPIKeyAuth
    ) -> Mapping[str, str]:
        return {file_id: self.unified_file_ids[file_id] for file_id in provider_file_ids if file_id in self.unified_file_ids}


class _UnreachableManagedFilesTable:
    async def get_unified_file_ids_for_provider_file_ids(
        self, provider_file_ids: Sequence[str], user_api_key_dict: UserAPIKeyAuth
    ) -> Mapping[str, str]:
        raise httpx.ConnectError("database is unreachable")


def _search_hit(file_id: str) -> Mapping[str, object]:
    return {"file_id": file_id, "filename": f"{file_id}.txt", "score": 0.5, "content": []}


def _search_page(*hits: Mapping[str, object]) -> Mapping[str, object]:
    return {
        "object": "vector_store.search_results.page",
        "search_query": "q",
        "data": list(hits),
        "has_more": False,
        "next_page": None,
    }


@pytest.mark.asyncio
async def test_search_hits_carry_the_managed_file_id_ingest_returned() -> None:
    managed_ids: Final = _ManagedFileIds(
        {"file-ingested": _managed_file_id("file-ingested"), "file-mismatched": _managed_file_id("file-other")}
    )

    mapped: Final = await with_managed_search_file_ids(
        _search_page(_search_hit("file-ingested"), _search_hit("file-unregistered"), _search_hit("file-mismatched")),
        managed_ids,
        UserAPIKeyAuth(api_key="team-a-member-key", team_id="team-a"),
    )

    assert mapped == _search_page(
        {**_search_hit("file-ingested"), "file_id": _managed_file_id("file-ingested")},
        _search_hit("file-unregistered"),
        _search_hit("file-mismatched"),
    )


@pytest.mark.asyncio
async def test_search_hits_keep_provider_file_ids_without_the_managed_files_hook() -> None:
    page: Final = _search_page(_search_hit("file-ingested"))

    assert await with_managed_search_file_ids(page, None, UserAPIKeyAuth(api_key="k", team_id="team-a")) == page


@pytest.mark.asyncio
async def test_search_hits_keep_provider_file_ids_when_the_managed_file_lookup_fails() -> None:
    page: Final = _search_page(_search_hit("file-ingested"))

    assert (
        await with_managed_search_file_ids(
            page, _UnreachableManagedFilesTable(), UserAPIKeyAuth(api_key="k", team_id="team-a")
        )
        == page
    )
