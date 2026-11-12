"""The Rust core's Slack alerting: ``alerting_config`` built into a ``SlackAlerting`` logger on the
host, as the Python core's ``_initialize_alerting`` builds it."""

from typing import TYPE_CHECKING, Final

from linten._logging import verbose_router_logger

if TYPE_CHECKING:
    from linten.integrations.SlackAlerting.slack_alerting import SlackAlerting
    from linten.router_python_host import PythonHost
    from linten.types.router import AlertingConfig


def initialize_alerting(host: "PythonHost", alerting_config: "AlertingConfig | None") -> "SlackAlerting | None":
    """``_initialize_alerting``: a ``SlackAlerting`` logger with the config's threshold and webhook,
    added to the host's callbacks, and its slow-response check to the host's success callbacks.
    No config builds nothing."""
    from linten.integrations.SlackAlerting.slack_alerting import SlackAlerting

    if alerting_config is None:
        return None
    logger: Final = SlackAlerting(
        alerting_threshold=alerting_config.alerting_threshold,
        alerting=["slack"],
        default_webhook_url=alerting_config.webhook_url,
    )
    host.callbacks.add_linten_callback(logger)
    host.callbacks.add_linten_success_callback(logger.response_taking_too_long_callback)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]  # SlackAlerting's untyped callback
    verbose_router_logger.info("\033[94m\nInitialized Alerting for linten.Router\033[0m\n")
    return logger


__all__ = ["initialize_alerting"]
