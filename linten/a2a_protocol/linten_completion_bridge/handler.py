"""
Handler for A2A to Linten completion bridge.

Routes A2A requests through linten.acompletion based on custom_llm_provider.

A2A Streaming Events (in order):
1. Task event (kind: "task") - Initial task creation with status "submitted"
2. Status update (kind: "status-update") - Status change to "working"
3. Artifact update (kind: "artifact-update") - Content/artifact delivery
4. Status update (kind: "status-update") - Final status "completed" with final=true
"""

from collections.abc import AsyncIterator, Mapping
from types import MappingProxyType
from typing import Any, Final

import linten
from linten._logging import verbose_logger
from linten.a2a_protocol.card_resolver import A2A_PROTOCOL_VERSION_PARAM, AGENT_CARD_PATH_PARAM
from linten.a2a_protocol.linten_completion_bridge.transformation import (
    A2ACompletionBridgeTransformation,
    A2AStreamingContext,
)
from linten.a2a_protocol.providers.config_manager import A2AProviderConfigManager
from linten.constants import A2A_CHAT_COMPLETION_BRIDGE_PROVIDERS, A2A_COMPLETION_BRIDGE_WORKING_MESSAGE
from linten.interactions.agents.utils import merge_agent_headers
from linten.linten_core_utils.streaming_handler import CustomStreamWrapper
from linten.types.utils import ModelResponse

# linten_params key carrying the authenticated principal (hashed virtual key) so
# A2A provider configs can scope provider-side state (e.g. LangFlow session memory)
# per key instead of trusting the client-supplied A2A contextId.
A2A_USER_API_KEY_HASH_PARAM: Final = "linten_a2a_user_api_key_hash"

# Agent metadata fields stored in linten_params that are not valid linten.acompletion() kwargs
_AGENT_ONLY_PARAMS: Final = frozenset(
    {
        "is_public",
        "agent_name",
        "agent_id",
        "agent_card_params",
        AGENT_CARD_PATH_PARAM,
        A2A_PROTOCOL_VERSION_PARAM,
        A2A_USER_API_KEY_HASH_PARAM,
    }
)


def bridge_model_name(linten_params: Mapping[str, object]) -> str:
    """The linten model string a bridge agent completes with: ``<custom_llm_provider>/<model>``.

    A provider bridged on chat names a real upstream endpoint with ``model``, so a missing one stays empty for that
    provider to reject or ignore instead of becoming a made-up ``agent`` endpoint.
    """
    custom_llm_provider: Final = linten_params.get("custom_llm_provider")
    default_model: Final = "" if custom_llm_provider in A2A_CHAT_COMPLETION_BRIDGE_PROVIDERS else "agent"
    configured_model: Final = linten_params.get("model")
    model: Final = configured_model if isinstance(configured_model, str) else default_model
    if not custom_llm_provider or model.startswith(f"{custom_llm_provider}/"):
        return model
    return f"{custom_llm_provider}/{model}"


def agent_completion_kwargs(linten_params: Mapping[str, object]) -> Mapping[str, object]:
    """The agent's linten_params that are valid linten.acompletion kwargs (api_key, api_base, ...)."""
    return MappingProxyType(
        {
            key: value
            for key, value in linten_params.items()
            if key not in ("model", "custom_llm_provider") and key not in _AGENT_ONLY_PARAMS
        }
    )


class A2ACompletionBridgeHandler:
    """
    Static methods for handling A2A requests via Linten completion.
    """

    @staticmethod
    def _build_completion_params(
        params: dict[str, Any],
        linten_params: Mapping[str, object],
        api_base: str | None,
        agent_extra_headers: Mapping[str, str] | None,
        *,
        stream: bool,
    ) -> Mapping[str, object]:
        # Extract message from params
        message: Final = params.get("message", {})

        # Transform A2A message to OpenAI format
        openai_messages: Final = A2ACompletionBridgeTransformation.a2a_message_to_openai_messages(message)

        full_model: Final = bridge_model_name(linten_params)

        if stream:
            verbose_logger.info("A2A completion bridge streaming: model=%s, api_base=%s", full_model, api_base)
        else:
            verbose_logger.info("A2A completion bridge: model=%s, api_base=%s", full_model, api_base)

        # Build completion params dict
        completion_params: Final[dict[str, Any]] = {
            "model": full_model,
            "messages": openai_messages,
            "api_base": api_base,
            "stream": stream,
        }
        completion_params.update(agent_completion_kwargs(linten_params))
        # Apply forward metadata AFTER the linten_params merge so the helper
        # sees any agent-owner-configured ``extra_body.metadata`` and can keep
        # those keys authoritative over the client-supplied A2A metadata.
        A2ACompletionBridgeTransformation.apply_forward_metadata_to_completion_params(
            completion_params=completion_params,
            a2a_message=message,
            params=params,
        )

        if agent_extra_headers:
            completion_params["extra_headers"] = merge_agent_headers(
                dynamic_headers=agent_extra_headers,
                static_headers=completion_params.get("extra_headers"),
            )

        return completion_params

    @staticmethod
    async def _acompletion(completion_params: Mapping[str, object]) -> ModelResponse | CustomStreamWrapper:
        return await linten.acompletion(**completion_params)

    @staticmethod
    async def handle_non_streaming(
        request_id: str,
        params: dict[str, object],
        linten_params: dict[str, Any],
        api_base: str | None = None,
        agent_extra_headers: dict[str, str] | None = None,
        *,
        _skip_a2a_provider_routing: bool = False,
    ) -> dict[str, object]:
        """
        Handle non-streaming A2A request via linten.acompletion.

        Args:
            request_id: A2A JSON-RPC request ID
            params: A2A MessageSendParams containing the message
            linten_params: Agent's linten_params (custom_llm_provider, model, etc.)
            api_base: API base URL from agent_card_params
            agent_extra_headers: Per-request headers (from x-a2a-{agent}-* rewrite and
                admin extra_headers) to forward on the upstream HTTP call.

        Returns:
            A2A SendMessageResponse dict
        """
        custom_llm_provider: Final = linten_params.get("custom_llm_provider")
        if not _skip_a2a_provider_routing:
            a2a_provider_config: Final = A2AProviderConfigManager.get_provider_config(
                custom_llm_provider=custom_llm_provider,
                model=linten_params.get("model"),
            )

            if a2a_provider_config is not None:
                verbose_logger.info("A2A: Using provider config for %s", custom_llm_provider)

                return await a2a_provider_config.handle_non_streaming(
                    request_id=request_id,
                    params=params,
                    api_base=api_base,
                    linten_params=linten_params,
                    agent_extra_headers=agent_extra_headers,
                )

        completion_params: Final = A2ACompletionBridgeHandler._build_completion_params(
            params=params,
            linten_params=linten_params,
            api_base=api_base,
            agent_extra_headers=agent_extra_headers,
            stream=False,
        )

        # Call linten.acompletion
        response: Final = await A2ACompletionBridgeHandler._acompletion(completion_params)

        # Transform response to A2A format
        a2a_response: Final = A2ACompletionBridgeTransformation.openai_response_to_a2a_response(
            response=response,
            request_id=request_id,
        )

        verbose_logger.info("A2A completion bridge completed: request_id=%s", request_id)

        return a2a_response

    @staticmethod
    async def handle_streaming(
        request_id: str,
        params: dict[str, Any],
        linten_params: dict[str, Any],
        api_base: str | None = None,
        agent_extra_headers: dict[str, str] | None = None,
        *,
        _skip_a2a_provider_routing: bool = False,
    ) -> AsyncIterator[dict[str, object]]:
        """
        Handle streaming A2A request via linten.acompletion with stream=True.

        Emits proper A2A streaming events:
        1. Task event (kind: "task") - Initial task with status "submitted"
        2. Status update (kind: "status-update") - Status "working"
        3. Artifact update (kind: "artifact-update") - Content delivery
        4. Status update (kind: "status-update") - Final "completed" status

        Args:
            request_id: A2A JSON-RPC request ID
            params: A2A MessageSendParams containing the message
            linten_params: Agent's linten_params (custom_llm_provider, model, etc.)
            api_base: API base URL from agent_card_params
            agent_extra_headers: Per-request headers (from x-a2a-{agent}-* rewrite and
                admin extra_headers) to forward on the upstream HTTP call.

        Yields:
            A2A streaming response events
        """
        custom_llm_provider: Final = linten_params.get("custom_llm_provider")
        if not _skip_a2a_provider_routing:
            a2a_provider_config: Final = A2AProviderConfigManager.get_provider_config(
                custom_llm_provider=custom_llm_provider,
                model=linten_params.get("model"),
            )

            if a2a_provider_config is not None:
                verbose_logger.info("A2A: Using provider config for %s (streaming)", custom_llm_provider)

                async for chunk in a2a_provider_config.handle_streaming(
                    request_id=request_id,
                    params=params,
                    api_base=api_base,
                    linten_params=linten_params,
                    agent_extra_headers=agent_extra_headers,
                ):
                    yield chunk

                return

        # Create streaming context
        ctx: Final = A2AStreamingContext(
            request_id=request_id,
            input_message=params.get("message", {}),
        )

        completion_params: Final = A2ACompletionBridgeHandler._build_completion_params(
            params=params,
            linten_params=linten_params,
            api_base=api_base,
            agent_extra_headers=agent_extra_headers,
            stream=True,
        )

        # 1. Emit initial task event (kind: "task", status: "submitted")
        task_event: Final = A2ACompletionBridgeTransformation.create_task_event(ctx)
        yield task_event

        # 2. Emit status update (kind: "status-update", status: "working")
        working_event: Final = A2ACompletionBridgeTransformation.create_status_update_event(
            ctx=ctx,
            state="working",
            final=False,
            message_text=A2A_COMPLETION_BRIDGE_WORKING_MESSAGE,
        )
        yield working_event

        # Call linten.acompletion with streaming
        response: Final = await A2ACompletionBridgeHandler._acompletion(completion_params)

        # 3. Accumulate content and emit artifact update
        accumulated_text = ""
        chunk_count = 0
        async for chunk in response:
            chunk_count += 1

            # Extract delta content
            content = ""
            if chunk is not None and hasattr(chunk, "choices") and chunk.choices:
                choice = chunk.choices[0]
                if hasattr(choice, "delta") and choice.delta:
                    content = choice.delta.content or ""

            if content:
                accumulated_text += content

        # Emit artifact update with accumulated content
        if accumulated_text:
            artifact_event: Final = A2ACompletionBridgeTransformation.create_artifact_update_event(
                ctx=ctx,
                text=accumulated_text,
            )
            yield artifact_event

        # 4. Emit final status update (kind: "status-update", status: "completed", final: true)
        completed_event: Final = A2ACompletionBridgeTransformation.create_status_update_event(
            ctx=ctx,
            state="completed",
            final=True,
        )
        yield completed_event

        verbose_logger.info(
            "A2A completion bridge streaming completed: request_id=%s, chunks=%s", request_id, chunk_count
        )


# Convenience functions that delegate to the class methods
async def handle_a2a_completion(
    request_id: str,
    params: dict[str, object],
    linten_params: dict[str, object],
    api_base: str | None = None,
    agent_extra_headers: dict[str, str] | None = None,
) -> dict[str, object]:
    """Convenience function for non-streaming A2A completion."""
    return await A2ACompletionBridgeHandler.handle_non_streaming(
        request_id=request_id,
        params=params,
        linten_params=linten_params,
        api_base=api_base,
        agent_extra_headers=agent_extra_headers,
    )


async def handle_a2a_completion_streaming(
    request_id: str,
    params: dict[str, object],
    linten_params: dict[str, object],
    api_base: str | None = None,
    agent_extra_headers: dict[str, str] | None = None,
) -> AsyncIterator[dict[str, object]]:
    """Convenience function for streaming A2A completion."""
    async for chunk in A2ACompletionBridgeHandler.handle_streaming(
        request_id=request_id,
        params=params,
        linten_params=linten_params,
        api_base=api_base,
        agent_extra_headers=agent_extra_headers,
    ):
        yield chunk
