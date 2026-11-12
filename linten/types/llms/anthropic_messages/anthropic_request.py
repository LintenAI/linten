from linten.types.llms.base import LintenBaseModel


class AnthropicMetadata(LintenBaseModel):
    """
    Object with allowed fields for Anthropic API metadata

    https://docs.anthropic.com/en/api/messages#body-metadata-user-id
    """

    user_id: str | None = None
