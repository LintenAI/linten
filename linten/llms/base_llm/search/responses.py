from collections.abc import Iterator, Sequence

from pydantic import ConfigDict

from linten.types.llms.base import LintenBaseModel


class ResponsesSearchAnnotation(LintenBaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    type: str = ""
    url: str | None = None
    title: str | None = None
    start_index: int | None = None
    end_index: int | None = None


class ResponsesSearchContent(LintenBaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    type: str = ""
    text: str = ""
    annotations: tuple[ResponsesSearchAnnotation, ...] = ()


class ResponsesSearchOutput(LintenBaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    type: str = ""
    content: tuple[ResponsesSearchContent, ...] = ()


class ResponsesSearchError(LintenBaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    message: str | None = None


class ResponsesSearchIncompleteDetails(LintenBaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    reason: str | None = None


class ResponsesSearchEnvelope(LintenBaseModel):
    """A Responses API body. `output` is required: a body without it is not a
    Responses API response and must not be reported as a successful empty search.

    A 200 body can still carry `status` `failed` or `incomplete`; those are surfaced as
    errors rather than reported as a successful empty search."""

    model_config = ConfigDict(extra="ignore", frozen=True)

    output: tuple[ResponsesSearchOutput, ...]
    status: str | None = None
    error: ResponsesSearchError | None = None
    incomplete_details: ResponsesSearchIncompleteDetails | None = None


def responses_search_text_parts(output: Sequence[ResponsesSearchOutput]) -> Iterator[ResponsesSearchContent]:
    for item in output:
        if item.type == "message":
            yield from (part for part in item.content if part.type == "output_text")


def responses_search_citations(
    output: Sequence[ResponsesSearchOutput],
) -> Iterator[tuple[ResponsesSearchContent, ResponsesSearchAnnotation]]:
    for part in responses_search_text_parts(output):
        yield from (
            (part, annotation)
            for annotation in part.annotations
            if annotation.type == "url_citation" and annotation.url
        )
