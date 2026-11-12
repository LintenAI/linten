from typing import Annotated, Literal

from pydantic import ConfigDict, Field

from linten.types.llms.base import LintenBaseModel


class VertexGemmaContainerError(LintenBaseModel):
    model_config = ConfigDict(frozen=True)
    object: Literal["error"]
    message: str
    code: Annotated[int, Field(ge=400, le=599)]
