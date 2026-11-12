"""
Linten Interactions API

This module provides SDK methods for Google's Interactions API.

Usage:
    import linten

    # Create an interaction with a model
    response = linten.interactions.create(
        model="gemini-2.5-flash",
        input="Hello, how are you?"
    )

    # Create an interaction with an agent
    response = linten.interactions.create(
        agent="deep-research-pro-preview-12-2025",
        input="Research the current state of cancer research"
    )

    # Async version
    response = await linten.interactions.acreate(...)

    # Get an interaction
    response = linten.interactions.get(interaction_id="...")

    # Delete an interaction
    result = linten.interactions.delete(interaction_id="...")

    # Cancel an interaction
    result = linten.interactions.cancel(interaction_id="...")

    # Create a managed agent on the provider side
    result = linten.interactions.agents.create(
        id="waverunner",
        custom_llm_provider="gemini",
        api_key="...",
        base_agent="antigravity-preview-09-2026",
        system_instruction="You are a helpful assistant.",
    )

Methods:
- create(): Sync create interaction
- acreate(): Async create interaction
- get(): Sync get interaction
- aget(): Async get interaction
- delete(): Sync delete interaction
- adelete(): Async delete interaction
- cancel(): Sync cancel interaction
- acancel(): Async cancel interaction

Sub-modules:
- agents: Provider-side agent creation (linten.interactions.agents.create)
"""

from linten.interactions import agents
from linten.interactions.main import (
    acancel,
    acreate,
    adelete,
    aget,
    cancel,
    create,
    delete,
    get,
)

__all__ = [
    "acancel",
    "acreate",
    "adelete",
    "agents",
    "aget",
    "cancel",
    "create",
    "delete",
    "get",
]
