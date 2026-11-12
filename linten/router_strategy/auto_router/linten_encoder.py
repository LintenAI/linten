from typing import TYPE_CHECKING, Any, ClassVar, Final, Optional

from pydantic import ConfigDict
from semantic_router.encoders import DenseEncoder
from semantic_router.encoders.base import AsymmetricDenseMixin

import linten
from linten._logging import verbose_router_logger
from linten.router_deprecated import RenamedRouterAttribute, renamed_router_param

if TYPE_CHECKING:
    from linten.router_api import RoutingContext
else:
    RoutingContext = Any


def linten_to_list(embeds: object) -> list[list[float]]:
    """Convert a Linten embedding response to a list of embeddings.

    :param embeds: The Linten embedding response.
    :return: A list of embeddings.
    """
    if not embeds or not isinstance(embeds, linten.EmbeddingResponse) or not embeds.data:
        raise ValueError("No embeddings found in Linten embedding response.")
    return [x["embedding"] for x in embeds.data]


class CustomDenseEncoder(DenseEncoder):
    model_config = ConfigDict(extra="allow")
    linten_router_instance: ClassVar = RenamedRouterAttribute()  # deprecated: the router attribute before ``ctx``

    @renamed_router_param("linten_router_instance")
    def __init__(self, ctx: Optional["RoutingContext"] = None, **kwargs) -> None:
        if "ctx" in kwargs:
            ctx = kwargs.pop("ctx")

        super().__init__(**kwargs)
        self.ctx = ctx


class LintenRouterEncoder(CustomDenseEncoder, AsymmetricDenseMixin):
    """Linten encoder class for generating embeddings using Linten.

    The LintenRouterEncoder class is a subclass of DenseEncoder and utilizes the Linten Router SDK
    to generate embeddings for given documents. It supports all encoders supported by Linten
    and supports customization of the score threshold for filtering or processing the embeddings.
    """

    type: str = "internal_linten_router"

    @renamed_router_param("linten_router_instance")
    def __init__(
        self,
        ctx: "RoutingContext",
        model_name: str,
        score_threshold: float | None = None,
        max_input_chars: int = 0,
    ) -> None:
        """Initialize the LintenEncoder.

        :param ctx: The routing context of the owning router.
        :type ctx: RoutingContext
        :param model_name: The name of the embedding model to use. Must use Linten naming
            convention (e.g. "openai/text-embedding-3-small" or "mistral/mistral-embed").
        :type model_name: str
        :param score_threshold: The score threshold for the embeddings.
        :type score_threshold: float
        :param max_input_chars: Longest doc, in characters, sent to the embedding model; anything
            longer is cut to this length. Opt-in, defaulting to 0 (send docs whole), because a
            caller that has to see the entire text to be correct must not be cut silently: a
            semantic guard that inspects only a prefix can be walked past with a benign opener.
            Callers that only rank text against short utterances, such as the auto-router, pass a
            limit so the encoder's context window cannot fail their request.
        :type max_input_chars: int
        """
        super().__init__(
            name=model_name,
            score_threshold=score_threshold if score_threshold is not None else 0.3,
        )
        self.model_name = model_name
        self.ctx = ctx
        self.max_input_chars = max_input_chars

    def _clamp(self, docs: list[str]) -> list[str]:  # mutable-ok: embedding() takes `input: str | list`
        """Cut every doc to `max_input_chars`, keeping the head, or return them whole when unset.

        The head carries the ask often enough to place it against a route, and a cut prompt still
        routes where an over-long one just errors out.
        """
        limit: Final = self.max_input_chars
        if limit <= 0:
            return docs
        clamped: Final = [doc[:limit] for doc in docs]
        if clamped != docs:
            verbose_router_logger.debug(
                "LintenRouterEncoder: cut input to %s chars for embedding model %s", limit, self.model_name
            )
        return clamped

    def __call__(self, docs: list[str], **kwargs) -> list[list[float]]:
        """Encode a list of text documents into embeddings using Linten.

        :param docs: List of text documents to encode.
        :return: List of embeddings for each document."""
        return self.encode_queries(docs, **kwargs)

    async def acall(self, docs: list[str], **kwargs) -> list[list[float]]:
        """Encode a list of documents into embeddings using Linten asynchronously.

        :param docs: List of documents to encode.
        :return: List of embeddings for each document."""
        return await self.aencode_queries(docs, **kwargs)

    def encode_queries(self, docs: list[str], **kwargs) -> list[list[float]]:
        if self.ctx is None:
            raise ValueError("ctx is not set")
        try:
            embeds: Final = self.ctx.embedding(input=self._clamp(docs), model=self.model_name, **kwargs)
            return linten_to_list(embeds)
        except Exception as e:
            raise ValueError(f"{self.type.capitalize()} API call failed. Error: {e}") from e

    def encode_documents(self, docs: list[str], **kwargs) -> list[list[float]]:
        if self.ctx is None:
            raise ValueError("ctx is not set")
        try:
            embeds: Final = self.ctx.embedding(input=self._clamp(docs), model=self.model_name, **kwargs)
            return linten_to_list(embeds)
        except Exception as e:
            raise ValueError(f"{self.type.capitalize()} API call failed. Error: {e}") from e

    async def aencode_queries(self, docs: list[str], **kwargs) -> list[list[float]]:
        if self.ctx is None:
            raise ValueError("ctx is not set")
        try:
            embeds: Final = await self.ctx.aembedding(input=self._clamp(docs), model=self.model_name, **kwargs)
            return linten_to_list(embeds)
        except Exception as e:
            raise ValueError(f"{self.type.capitalize()} API call failed. Error: {e}") from e

    async def aencode_documents(self, docs: list[str], **kwargs) -> list[list[float]]:
        if self.ctx is None:
            raise ValueError("ctx is not set")
        try:
            embeds: Final = await self.ctx.aembedding(input=self._clamp(docs), model=self.model_name, **kwargs)
            return linten_to_list(embeds)
        except Exception as e:
            raise ValueError(f"{self.type.capitalize()} API call failed. Error: {e}") from e
