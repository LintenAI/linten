from linten.types.llms.base import LintenBaseModel


class TestPromptRequest(LintenBaseModel):
    dotprompt_content: str
    prompt_variables: dict[str, object] | None = None
    conversation_history: list[dict[str, str]] | None = None
