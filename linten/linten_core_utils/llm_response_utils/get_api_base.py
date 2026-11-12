from typing import Final

import linten
from linten import verbose_logger

from ...linten_core_utils.get_llm_provider_logic import (
    declared_authenticating_provider,
    get_llm_provider,
)
from ...types.router import Linten_Params


def _api_base_without_login(provider: str) -> str | None:
    if provider == "github_copilot":
        return linten.GithubCopilotConfig().api_base_without_login()
    if provider == "chatgpt":
        return linten.ChatGPTConfig().api_base_without_login()
    return None


def _provider_default_api_base(model: str, custom_llm_provider: str | None, stream: bool) -> str | None:
    if custom_llm_provider == "gemini":
        action: Final = "streamGenerateContent" if stream else "generateContent"
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:{action}"
    if custom_llm_provider == "openai":
        return "https://api.openai.com"
    return None


def get_api_base(model: str, optional_params: dict | Linten_Params) -> str | None:
    """
    Returns the api base used for calling the model.

    Parameters:
    - model: str - the model passed to linten.completion()
    - optional_params - the 'linten_params' in router.completion *OR* additional params passed to linten.completion - eg. api_base, api_key, etc. See `Linten_Params` - https://github.com/LintenAI/linten/blob/f09e6ba98d65e035a79f73bc069145002ceafd36/linten/router.py#L67

    Returns:
    - string (api_base) or None

    Example:
    ```
    from linten import get_api_base

    get_api_base(model="gemini/gemini-pro")
    ```
    """

    try:
        if isinstance(optional_params, Linten_Params):
            _optional_params = optional_params
        elif "model" in optional_params:
            _optional_params = Linten_Params(**optional_params)
        else:  # prevent needing to copy and pop the dict
            _optional_params = Linten_Params(model=model, **optional_params)  # convert to pydantic object
    except Exception:
        return None
    # get llm provider

    if _optional_params.api_base is not None:
        return _optional_params.api_base
    extra_params: Final = _optional_params.model_extra
    base_url_alias: Final = extra_params.get("base_url") if extra_params is not None else None
    if isinstance(base_url_alias, str) and base_url_alias:
        return base_url_alias

    if linten.model_alias_map and model in linten.model_alias_map:
        model = linten.model_alias_map[model]
    declared: Final = declared_authenticating_provider(model, _optional_params.custom_llm_provider)
    if declared is not None:
        return _api_base_without_login(declared)
    try:
        (
            model,
            custom_llm_provider,
            dynamic_api_key,
            dynamic_api_base,
        ) = get_llm_provider(
            model=model,
            custom_llm_provider=_optional_params.custom_llm_provider,
            api_base=_optional_params.api_base,
            api_key=_optional_params.api_key,
        )
    except Exception as e:
        verbose_logger.debug("Error occurred in getting api base - %s", e)
        custom_llm_provider = None
        dynamic_api_base = None

    if dynamic_api_base is not None:
        return dynamic_api_base

    stream: Final[bool] = getattr(optional_params, "stream", False)

    if _optional_params.vertex_location is not None and _optional_params.vertex_project is not None:
        from linten.llms.vertex_ai.vertex_llm_base import VertexBase
        from linten.types.llms.vertex_ai import VertexPartnerProvider

        if "claude" in model:
            _api_base = VertexBase.create_vertex_url(
                vertex_location=_optional_params.vertex_location,
                vertex_project=_optional_params.vertex_project,
                model=model,
                stream=stream,
                partner=VertexPartnerProvider.claude,
            )
        else:
            if stream:
                _api_base = f"{_optional_params.vertex_location}-aiplatform.googleapis.com/v1/projects/{_optional_params.vertex_project}/locations/{_optional_params.vertex_location}/publishers/google/models/{model}:streamGenerateContent"
            else:
                _api_base = f"{_optional_params.vertex_location}-aiplatform.googleapis.com/v1/projects/{_optional_params.vertex_project}/locations/{_optional_params.vertex_location}/publishers/google/models/{model}:generateContent"
        return _api_base

    return _provider_default_api_base(model, custom_llm_provider, stream)
