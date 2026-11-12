from linten._logging import verbose_proxy_logger
from linten.linten_core_utils.dd_tracing import set_active_span_tag
from linten.proxy._types import UserAPIKeyAuth


class DDSpanTagger:
    """Best-effort helpers for tagging the active Datadog APM span with Linten request metadata."""

    @staticmethod
    def tag_call_id(linten_call_id: str | None) -> None:
        """
        Attach Linten call id to the active Datadog APM span.

        This enables searching APM traces by Linten call id returned in
        `x-linten-call-id`.
        """
        if not linten_call_id:
            return
        try:
            set_active_span_tag("linten.call_id", str(linten_call_id))
        except Exception:
            verbose_proxy_logger.debug(
                "Failed to tag active ddtrace span with linten.call_id",
                exc_info=True,
            )

    @staticmethod
    def tag_request(
        user_api_key_dict: UserAPIKeyAuth,
        requested_model: str | None,
    ) -> None:
        """
        Attach key and model tags to the active Datadog APM span.

        Tags set (all best-effort, skipped when value is absent):
        - ``linten.key_alias``      — human-readable alias for the API key
        - ``linten.key_hash``       — hashed API key (safe to log; never the raw secret)
        - ``linten.requested_model``— model name as sent by the client
        - ``linten.user_email``     — email of the authenticated user

        Use cases:
        - Trace all requests from a specific user/key: filter by ``linten.key_alias`` or
          ``linten.key_hash``.
        - Trace all requests for a specific model: filter by ``linten.requested_model``.
        - Trace all requests from a specific person under JWT auth, where there is no key_alias:
          filter by ``@linten.user_email:"user@example.com"``. The value comes from the JWT claim
          mapped by ``linten_jwtauth.user_email_jwt_field``, or from the user row for virtual keys.

        Note: key_alias / key_hash are not available for unauthenticated (e.g. 401) requests.
        """
        try:
            if user_api_key_dict.key_alias:
                set_active_span_tag("linten.key_alias", str(user_api_key_dict.key_alias))
            if user_api_key_dict.token:
                set_active_span_tag("linten.key_hash", str(user_api_key_dict.token))
            if requested_model:
                set_active_span_tag("linten.requested_model", str(requested_model))
            if user_api_key_dict.user_email:
                set_active_span_tag("linten.user_email", str(user_api_key_dict.user_email))
        except Exception:
            verbose_proxy_logger.debug(
                "Failed to tag active ddtrace span with key/model/user tags",
                exc_info=True,
            )
