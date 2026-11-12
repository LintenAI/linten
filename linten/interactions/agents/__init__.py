"""
linten.interactions.agents

Full CRUD SDK for provider-side managed agents (e.g. Gemini v1beta/agents).

    linten.interactions.agents.create(id=..., ...)
    linten.interactions.agents.list(api_key=...)
    linten.interactions.agents.get(id=..., ...)
    linten.interactions.agents.delete(id=..., ...)
    linten.interactions.agents.list_versions(id=..., ...)

Async counterparts: acreate, alist, aget, adelete, alist_versions
"""

from linten.interactions.agents.main import (
    acreate,
    adelete,
    aget,
    alist,
    alist_versions,
    create,
    delete,
    get,
    list,
    list_versions,
)

__all__ = [
    "acreate",
    "adelete",
    "aget",
    "alist",
    "alist_versions",
    "create",
    "delete",
    "get",
    "list",
    "list_versions",
]
