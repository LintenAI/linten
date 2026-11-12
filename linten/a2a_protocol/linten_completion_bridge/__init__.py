"""
A2A to Linten Completion Bridge.

This module provides transformation between A2A protocol messages and
Linten completion API, enabling any Linten-supported provider to be
invoked via the A2A protocol.
"""

from linten.a2a_protocol.linten_completion_bridge.handler import (
    A2ACompletionBridgeHandler,
    handle_a2a_completion,
    handle_a2a_completion_streaming,
)
from linten.a2a_protocol.linten_completion_bridge.transformation import (
    A2ACompletionBridgeTransformation,
)

__all__ = [
    "A2ACompletionBridgeHandler",
    "A2ACompletionBridgeTransformation",
    "handle_a2a_completion",
    "handle_a2a_completion_streaming",
]
