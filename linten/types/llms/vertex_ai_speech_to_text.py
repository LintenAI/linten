from typing import Annotated, Literal

from pydantic import ConfigDict, Field
from typing_extensions import TypedDict

from linten.types.llms.base import LintenBaseModel


class VertexSpeechToTextAutoDecodingConfig(TypedDict):
    pass


class VertexSpeechToTextRecognitionFeatures(TypedDict):
    enableAutomaticPunctuation: bool


class VertexSpeechToTextRecognitionConfig(TypedDict):
    model: str
    languageCodes: list[str]
    features: VertexSpeechToTextRecognitionFeatures
    autoDecodingConfig: VertexSpeechToTextAutoDecodingConfig


class VertexSpeechToTextRecognizeRequest(TypedDict):
    config: VertexSpeechToTextRecognitionConfig
    content: str


class VertexSpeechToTextAlternative(LintenBaseModel):
    transcript: str | None = None


class VertexSpeechToTextResult(LintenBaseModel):
    alternatives: list[VertexSpeechToTextAlternative] = Field(default=[])
    languageCode: str | None = None


class VertexSpeechToTextResponseMetadata(LintenBaseModel):
    totalBilledDuration: str | None = None


class VertexSpeechToTextRecognizeResponse(LintenBaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)

    results: list[VertexSpeechToTextResult] = Field(default=[])
    metadata: VertexSpeechToTextResponseMetadata | None = None


class VertexSpeechStreamingConfigure(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["configure"] = "configure"
    model: str
    language_codes: tuple[str, ...]
    sample_rate_hertz: int


class VertexSpeechStreamingFinishTurn(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["finish_turn"] = "finish_turn"


class VertexSpeechStreamingDiscardTurn(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["discard_turn"] = "discard_turn"


VertexSpeechStreamingCommandUnion = (
    VertexSpeechStreamingConfigure | VertexSpeechStreamingFinishTurn | VertexSpeechStreamingDiscardTurn
)
VertexSpeechStreamingCommand = Annotated[VertexSpeechStreamingCommandUnion, Field(discriminator="kind")]


class VertexSpeechStreamingResult(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    transcript: str
    is_final: bool


class VertexSpeechStreamingResponse(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["response"] = "response"
    speech_event: Literal["none", "begin", "end"]
    results: tuple[VertexSpeechStreamingResult, ...]
    billed_seconds: float


class VertexSpeechStreamingConfigured(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["configured"] = "configured"


class VertexSpeechStreamingTurnFinished(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["turn_finished"] = "turn_finished"


class VertexSpeechStreamingTurnDiscarded(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    kind: Literal["turn_discarded"] = "turn_discarded"
    billed_seconds: float


VertexSpeechStreamingEventUnion = (
    VertexSpeechStreamingResponse
    | VertexSpeechStreamingConfigured
    | VertexSpeechStreamingTurnFinished
    | VertexSpeechStreamingTurnDiscarded
)
VertexSpeechStreamingEvent = Annotated[VertexSpeechStreamingEventUnion, Field(discriminator="kind")]
