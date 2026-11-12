from typing import Final, Literal

import linten
from linten.exceptions import BadRequestError
from linten.linten_core_utils.get_llm_provider_logic import declared_authenticating_provider
from linten.llms.bedrock_mantle.chat.claude_transformation import bedrock_mantle_chat_config
from linten.types.utils import LlmProviders, LlmProvidersSet


def get_supported_openai_params(
    model: str,
    custom_llm_provider: str | None = None,
    request_type: Literal["chat_completion", "embeddings", "transcription"] = "chat_completion",
    base_model: str | None = None,
) -> list | None:
    """
    Returns the supported openai params for a given model + provider

    Example:
    ```
    get_supported_openai_params(model="anthropic.claude-3", custom_llm_provider="bedrock")
    ```

    Args:
        base_model: An optional capability hint for deployments whose ``model``
            label isn't recognized on its own (e.g. an Azure deployment name, or a
            friendly Bedrock alias). It is additive: the result is the union of the
            params supported by ``model`` and by ``base_model``, so a hint can only
            add capabilities, never strip ones the real model already supports.

    Returns:
    - List if custom_llm_provider is mapped
    - None if unmapped
    """
    if not custom_llm_provider:
        custom_llm_provider = declared_authenticating_provider(model)
    if not custom_llm_provider:
        try:
            custom_llm_provider = linten.get_llm_provider(model=model)[1]
        except BadRequestError:
            return None

    if custom_llm_provider in LlmProvidersSet:
        provider_config = linten.ProviderConfigManager.get_provider_chat_config(
            model=model,
            provider=LlmProviders(custom_llm_provider),
            base_model=base_model,
        )
    elif custom_llm_provider.split("/")[0] in LlmProvidersSet:
        provider_config = linten.ProviderConfigManager.get_provider_chat_config(
            model=model,
            provider=LlmProviders(custom_llm_provider.split("/")[0]),
            base_model=base_model,
        )
    else:
        provider_config = None

    if provider_config and request_type == "chat_completion":
        supported_params = provider_config.get_supported_openai_params(model=model)
        if base_model and base_model != model:
            base_model_params: Final = provider_config.get_supported_openai_params(model=base_model)
            supported_params = list(dict.fromkeys([*supported_params, *base_model_params]))
        return supported_params

    if custom_llm_provider == "bedrock" or custom_llm_provider == "bedrock_converse":
        return linten.AmazonConverseConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "meta_llama":
        provider_config = linten.ProviderConfigManager.get_provider_chat_config(
            model=model, provider=LlmProviders.LLAMA
        )
        if provider_config:
            return provider_config.get_supported_openai_params(model=model)
    elif custom_llm_provider == "ollama":
        return linten.OllamaConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "ollama_chat":
        return linten.OllamaChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "anthropic":
        return linten.AnthropicConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "anthropic_text":
        return linten.AnthropicTextConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "fireworks_ai":
        if request_type == "embeddings":
            return linten.FireworksAIEmbeddingConfig().get_supported_openai_params(model=model)
        elif request_type == "transcription":
            return None
        else:
            return linten.FireworksAIConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "nvidia_nim":
        if request_type == "chat_completion":
            return linten.nvidiaNimConfig.get_supported_openai_params(model=model)
        elif request_type == "embeddings":
            return linten.nvidiaNimEmbeddingConfig.get_supported_openai_params()
    elif custom_llm_provider == "cerebras":
        return linten.CerebrasConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "nadir":
        return linten.NadirConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "baseten":
        return linten.BasetenConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "xai":
        return linten.XAIChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "ai21_chat" or custom_llm_provider == "ai21":
        return linten.AI21ChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "volcengine":
        return linten.VolcEngineConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "groq":
        return linten.GroqChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "bedrock_mantle":
        return bedrock_mantle_chat_config(model).get_supported_openai_params(model=model)
    elif custom_llm_provider == "hosted_vllm":
        return linten.HostedVLLMChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "vllm":
        return linten.VLLMConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "deepseek":
        return linten.DeepSeekChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "tencent":
        return linten.TencentChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "cohere_chat" or custom_llm_provider == "cohere":
        return linten.CohereChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "maritalk":
        return linten.MaritalkConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "openai":
        if request_type == "transcription":
            transcription_provider_config = linten.ProviderConfigManager.get_provider_audio_transcription_config(
                model=model, provider=LlmProviders.OPENAI
            )
            if isinstance(transcription_provider_config, linten.OpenAIGPTAudioTranscriptionConfig):
                return transcription_provider_config.get_supported_openai_params(model=model)
            else:
                raise ValueError(f"Unsupported provider config: {transcription_provider_config} for model: {model}")
        return linten.OpenAIConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "sap":
        if request_type == "chat_completion":
            return linten.GenAIHubOrchestrationConfig().get_supported_openai_params(model=model)
        elif request_type == "embeddings":
            return linten.GenAIHubEmbeddingConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "azure":
        _azure_detection_model: Final = base_model or model
        if linten.AzureOpenAIO1Config().is_o_series_model(model=_azure_detection_model):
            return linten.AzureOpenAIO1Config().get_supported_openai_params(model=_azure_detection_model)
        elif linten.AzureOpenAIGPT5Config.is_model_gpt_5_model(model=_azure_detection_model):
            return linten.AzureOpenAIGPT5Config().get_supported_openai_params(model=_azure_detection_model)
        else:
            return linten.AzureOpenAIConfig().get_supported_openai_params(model=_azure_detection_model)
    elif custom_llm_provider == "openrouter":
        return linten.OpenrouterConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "vercel_ai_gateway":
        return linten.VercelAIGatewayConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "mistral" or custom_llm_provider == "codestral":
        # mistal and codestral api have the exact same params
        if request_type == "chat_completion":
            return linten.MistralConfig().get_supported_openai_params(model=model)
        elif request_type == "embeddings":
            return linten.MistralEmbeddingConfig().get_supported_openai_params()
        elif request_type == "transcription":
            from linten.llms.mistral.audio_transcription.transformation import (
                MistralAudioTranscriptionConfig,
            )

            return MistralAudioTranscriptionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "text-completion-codestral":
        return linten.CodestralTextCompletionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "sambanova":
        if request_type == "embeddings":
            return linten.SambaNovaEmbeddingConfig().get_supported_openai_params(model=model)
        else:
            return linten.SambanovaConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "nebius":
        if request_type == "chat_completion":
            return linten.NebiusConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "wandb":
        if request_type == "chat_completion":
            return linten.WandbConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "replicate":
        return linten.ReplicateConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "huggingface":
        return linten.HuggingFaceChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "jina_ai":
        if request_type == "embeddings":
            return linten.JinaAIEmbeddingConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "together_ai":
        return linten.TogetherAIChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "databricks":
        if request_type == "chat_completion":
            return linten.DatabricksConfig().get_supported_openai_params(model=model)
        elif request_type == "embeddings":
            return linten.DatabricksEmbeddingConfig().get_supported_openai_params()
    elif custom_llm_provider == "palm" or custom_llm_provider == "gemini":
        return linten.GoogleAIStudioGeminiConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "novita":
        return linten.NovitaConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "vertex_ai" or custom_llm_provider == "vertex_ai_beta":
        if request_type == "chat_completion":
            if model.startswith("mistral"):
                return linten.VertexAIMistralConfig().get_supported_openai_params(model=model)
            elif model.startswith("codestral"):
                return linten.CodestralTextCompletionConfig().get_supported_openai_params(model=model)
            elif model.startswith("claude"):
                return linten.VertexAIAnthropicConfig().get_supported_openai_params(model=model)
            elif model.startswith("gemini"):
                return linten.VertexGeminiConfig().get_supported_openai_params(model=model)
            else:
                return linten.VertexAILlama3Config().get_supported_openai_params(model=model)
        elif request_type == "embeddings":
            return linten.VertexAITextEmbeddingConfig().get_supported_openai_params()
    elif custom_llm_provider == "sagemaker":
        return linten.SagemakerConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "aleph_alpha":
        return [
            "max_tokens",
            "stream",
            "top_p",
            "temperature",
            "presence_penalty",
            "frequency_penalty",
            "n",
            "stop",
        ]
    elif custom_llm_provider == "cloudflare":
        return linten.CloudflareChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "nlp_cloud":
        return linten.NLPCloudConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "petals":
        return linten.PetalsConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "deepinfra":
        return linten.DeepInfraConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "perplexity":
        return linten.PerplexityChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "nscale":
        return linten.NscaleConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "anyscale":
        return [
            "temperature",
            "top_p",
            "stream",
            "max_tokens",
            "stop",
            "frequency_penalty",
            "presence_penalty",
        ]
    elif custom_llm_provider == "watsonx":
        return linten.IBMWatsonXChatConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "watsonx_text":
        return linten.IBMWatsonXAIConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "custom_openai" or custom_llm_provider == "text-completion-openai":
        return linten.OpenAITextCompletionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "predibase":
        return linten.PredibaseConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "voyage":
        if request_type == "embeddings" and linten.VoyageMultimodalEmbeddingConfig.is_multimodal_embeddings(model):
            return linten.VoyageMultimodalEmbeddingConfig().get_supported_openai_params(model=model)
        return linten.VoyageEmbeddingConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "infinity":
        return linten.InfinityEmbeddingConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "triton":
        if request_type == "embeddings":
            return linten.TritonEmbeddingConfig().get_supported_openai_params(model=model)
        else:
            return linten.TritonConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "deepgram":
        if request_type == "transcription":
            return linten.DeepgramAudioTranscriptionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "ovhcloud":
        if request_type == "transcription":
            from linten.llms.ovhcloud.audio_transcription.transformation import (
                OVHCloudAudioTranscriptionConfig,
            )

            return OVHCloudAudioTranscriptionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "scaleway":
        if request_type == "transcription":
            from linten.llms.scaleway.audio_transcription.transformation import (
                ScalewayAudioTranscriptionConfig,
            )

            return ScalewayAudioTranscriptionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "elevenlabs":
        if request_type == "transcription":
            from linten.llms.elevenlabs.audio_transcription.transformation import (
                ElevenLabsAudioTranscriptionConfig,
            )

            return ElevenLabsAudioTranscriptionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider == "soniox":
        if request_type == "transcription":
            from linten.llms.soniox.audio_transcription.transformation import (
                SonioxAudioTranscriptionConfig,
            )

            return SonioxAudioTranscriptionConfig().get_supported_openai_params(model=model)
    elif custom_llm_provider in linten._custom_providers:
        if request_type == "chat_completion":
            provider_config = linten.ProviderConfigManager.get_provider_chat_config(
                model=model, provider=LlmProviders.CUSTOM
            )
            if provider_config:
                return provider_config.get_supported_openai_params(model=model)
        elif request_type == "embeddings" or request_type == "transcription":
            return None

    return None
