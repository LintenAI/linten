from typing import Final

from linten.llms.azure.common_utils import BaseAzureLLM
from linten.llms.openai.vector_stores.transformation import OpenAIVectorStoreConfig
from linten.types.router import GenericLintenParams


class AzureOpenAIVectorStoreConfig(OpenAIVectorStoreConfig):
    def get_complete_url(
        self,
        api_base: str | None,
        linten_params: dict,
    ) -> str:
        return BaseAzureLLM.get_base_azure_url(
            api_base=api_base,
            linten_params=linten_params,
            route="/openai/vector_stores",
        )

    def get_vector_store_url(self, api_base: str, encoded_vector_store_id: str) -> str:
        path, _, query = api_base.partition("?")
        url: Final = f"{path}/{encoded_vector_store_id}"
        return f"{url}?{query}" if query else url

    def validate_environment(self, headers: dict, linten_params: GenericLintenParams | None) -> dict:
        return BaseAzureLLM.base_validate_azure_environment(headers=headers, linten_params=linten_params)
