"""
Bridge module for connecting Interactions API to Responses API via linten.responses().
"""

from linten.interactions.linten_responses_transformation.handler import (
    LintenResponsesInteractionsHandler,
)
from linten.interactions.linten_responses_transformation.transformation import (
    LintenResponsesInteractionsConfig,
)

__all__ = [
    "LintenResponsesInteractionsConfig",  # Transformation config class (not BaseInteractionsAPIConfig)
    "LintenResponsesInteractionsHandler",
]
