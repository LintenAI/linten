from typing import Final

from linten.llms.cloudflare.extraction.guardrail_translation.handler import ExtractionHandler
from linten.types.utils import CallTypes

guardrail_translation_mappings: Final = {
    CallTypes.extraction: ExtractionHandler,
    CallTypes.aextraction: ExtractionHandler,
}

__all__ = ["ExtractionHandler", "guardrail_translation_mappings"]
