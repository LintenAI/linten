"""
Managed file, object, and vector store table models.

Canonical definitions for the ``linten_managed*`` tables. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from datetime import datetime
from typing import Literal

from linten.types.llms.base import LintenPydanticObjectBase
from linten.types.llms.openai import OpenAIFileObject, ResponsesAPIResponse
from linten.types.utils import LintenBatch, LintenFineTuningJob


class Linten_ManagedFileTable(LintenPydanticObjectBase):
    unified_file_id: str
    file_object: OpenAIFileObject | None = None
    model_mappings: dict[str, str]
    flat_model_file_ids: list[str]
    created_by: str | None = None
    team_id: str | None = None
    updated_by: str | None = None
    storage_backend: str | None = None
    storage_url: str | None = None


class Linten_ManagedObjectTable(LintenPydanticObjectBase):
    unified_object_id: str
    model_object_id: str
    file_purpose: Literal["batch", "fine-tune", "response", "container"]
    file_object: LintenBatch | LintenFineTuningJob | ResponsesAPIResponse
    created_by: str | None = None
    team_id: str | None = None
    org_id: str | None = None


class Linten_ManagedVectorStoreTable(LintenPydanticObjectBase):
    """Table for managing vector stores with target_model_names support."""

    unified_resource_id: str
    resource_object: object | None = None
    model_mappings: dict[str, str]
    flat_model_resource_ids: list[str]
    created_by: str | None = None
    team_id: str | None = None
    updated_by: str | None = None
    storage_backend: str | None = None
    storage_url: str | None = None


class Linten_ManagedVectorStoresTable(LintenPydanticObjectBase):
    vector_store_id: str
    custom_llm_provider: str
    vector_store_name: str | None = None
    vector_store_description: str | None = None
    vector_store_metadata: dict[str, object] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    linten_credential_name: str | None = None
    linten_params: dict[str, object] | None = None
    team_id: str | None = None
    user_id: str | None = None
    is_config: bool = False
