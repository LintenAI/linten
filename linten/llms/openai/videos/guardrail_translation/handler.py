from typing import TYPE_CHECKING, Final

from linten.llms.base_llm.guardrail_translation.base_translation import BaseTranslation
from linten.types.utils import GenericGuardrailAPIInputs

if TYPE_CHECKING:
    from linten.integrations.custom_guardrail import CustomGuardrail
    from linten.linten_core_utils.linten_logging import Logging as LintenLoggingObj
    from linten.types.proxy.auth.user_api_key_auth import UserAPIKeyAuth


class OpenAIVideoGenerationHandler(BaseTranslation):
    async def process_input_messages(
        self,
        data: dict[str, object],  # mutable-ok: BaseTranslation contract passes the proxy's request dict through
        guardrail_to_apply: "CustomGuardrail",
        linten_logging_obj: "LintenLoggingObj | None" = None,
    ) -> dict[str, object]:  # mutable-ok: BaseTranslation contract returns the proxy's request dict
        prompt: Final = data.get("prompt")
        if not isinstance(prompt, str):
            return data

        model: Final = data.get("model")
        texts: Final = [prompt]
        inputs: Final = (
            GenericGuardrailAPIInputs(texts=texts, model=model)
            if isinstance(model, str)
            else GenericGuardrailAPIInputs(texts=texts)
        )
        guardrailed_inputs: Final = await guardrail_to_apply.apply_guardrail(  # pyright: ignore[reportUnknownMemberType]  # request_data is a bare dict
            inputs=inputs,
            request_data=data,
            input_type="request",
            logging_obj=linten_logging_obj,
        )
        guardrailed_texts: Final = guardrailed_inputs.get("texts")
        guardrailed_prompt: Final = guardrailed_texts[0] if guardrailed_texts else prompt
        return {**data, "prompt": guardrailed_prompt}

    async def process_output_response(
        self,
        response: object,
        guardrail_to_apply: "CustomGuardrail",
        linten_logging_obj: "LintenLoggingObj | None" = None,
        user_api_key_dict: "UserAPIKeyAuth | None" = None,
        request_data: dict[str, object] | None = None,  # mutable-ok: BaseTranslation contract
    ) -> object:
        return response
