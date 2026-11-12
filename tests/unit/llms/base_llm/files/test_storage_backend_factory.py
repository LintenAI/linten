from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from linten.llms.base_llm.files.linten_db_storage_backend import (
    LINTEN_DB_STORAGE_BACKEND_NAME,
    LINTEN_DB_STORAGE_URL_PREFIX,
    LintenDbStorageBackend,
)
from linten.llms.base_llm.files.storage_backend_factory import get_storage_backend


@pytest.mark.asyncio
async def test_linten_db_backend_stores_through_the_given_prisma_client():
    table = MagicMock(create=AsyncMock(return_value=SimpleNamespace(id="row-1")))
    prisma_client = MagicMock(db=MagicMock(linten_managedfilecontenttable=table))

    backend = get_storage_backend(LINTEN_DB_STORAGE_BACKEND_NAME, prisma_client=prisma_client)

    assert isinstance(backend, LintenDbStorageBackend)
    stored_at = await backend.upload_file(file_content=b"line\n", filename="input.jsonl", content_type="text/plain")
    assert stored_at == f"{LINTEN_DB_STORAGE_URL_PREFIX}row-1"
    table.create.assert_awaited_once()


def test_linten_db_backend_without_a_database_is_rejected():
    with pytest.raises(ValueError, match="database-connected proxy"):
        get_storage_backend(LINTEN_DB_STORAGE_BACKEND_NAME)


def test_unknown_backend_is_still_rejected():
    with pytest.raises(ValueError, match="Unsupported storage backend type: nope"):
        get_storage_backend("nope", prisma_client=MagicMock())
