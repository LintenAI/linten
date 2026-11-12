from linten.linten_core_utils.url_utils import join_api_base
from linten.llms.openai.image_edit.transformation import OpenAIImageEditConfig
from linten.secret_managers.main import get_secret_str


class LintenProxyImageEditConfig(OpenAIImageEditConfig):
    """Configuration for image edit requests routed through Linten Proxy."""

    def validate_environment(
        self,
        headers: dict,
        model: str,
        api_key: str | None = None,
        linten_params: dict | None = None,
        api_base: str | None = None,
    ) -> dict:
        api_key = api_key or get_secret_str("LINTEN_PROXY_API_KEY")
        headers.update({"Authorization": f"Bearer {api_key}"})
        return headers

    def get_complete_url(self, model: str, api_base: str | None, linten_params: dict) -> str:
        api_base = api_base or get_secret_str("LINTEN_PROXY_API_BASE")
        if api_base is None:
            raise ValueError("api_base not set for Linten Proxy route. Set in env via `LINTEN_PROXY_API_BASE`")
        return join_api_base(api_base, "images/edits")
