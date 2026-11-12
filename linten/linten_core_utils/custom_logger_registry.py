"""
Registry mapping the callback class string to the class type.

This is used to get the class type from the callback class string.

Example:
    "datadog" -> DataDogLogger
    "prometheus" -> PrometheusLogger
"""

from typing import Final

from linten import _custom_logger_compatible_callbacks_literal
from linten.integrations.agentops import AgentOps
from linten.integrations.anthropic_cache_control_hook import AnthropicCacheControlHook
from linten.integrations.argilla import ArgillaLogger
from linten.integrations.azure_sentinel.azure_sentinel import AzureSentinelLogger
from linten.integrations.azure_storage.azure_storage import AzureBlobStorageLogger
from linten.integrations.bitbucket import BitBucketPromptManager
from linten.integrations.braintrust_logging import BraintrustLogger
from linten.integrations.cloudzero.cloudzero import CloudZeroLogger
from linten.integrations.datadog.datadog import DataDogLogger
from linten.integrations.datadog.datadog_llm_obs import DataDogLLMObsLogger
from linten.integrations.datadog.datadog_metrics import DatadogMetricsLogger
from linten.integrations.deepeval import DeepEvalLogger
from linten.integrations.dotprompt import DotpromptManager
from linten.integrations.focus.focus_logger import FocusLogger
from linten.integrations.galileo import GalileoObserve
from linten.integrations.gcs_bucket.gcs_bucket import GCSBucketLogger
from linten.integrations.gcs_pubsub.pub_sub import GcsPubSubLogger
from linten.integrations.gitlab import GitLabPromptManager
from linten.integrations.humanloop import HumanloopLogger
from linten.integrations.lago import LagoLogger
from linten.integrations.langfuse.langfuse_prompt_management import (
    LangfusePromptManagement,
)
from linten.integrations.langsmith import LangsmithLogger
from linten.integrations.linten_agent import LintenAgentModelResolver
from linten.integrations.literal_ai import LiteralAILogger
from linten.integrations.mavvrik_focus.mavvrik_focus_logger import MavvrikFocusLogger
from linten.integrations.mlflow import MlflowLogger
from linten.integrations.newrelic import NewRelicLogger
from linten.integrations.openmeter import OpenMeterLogger
from linten.integrations.opentelemetry import OpenTelemetry
from linten.integrations.opik.opik import OpikLogger
from linten.integrations.pointfive import PointFiveLogger
from linten.integrations.posthog import PostHogLogger
from linten.integrations.prometheus import PrometheusLogger
from linten.integrations.s3_v2 import S3Logger
from linten.integrations.sqs import SQSLogger
from linten.integrations.ternary.ternary_logger import TernaryLogger
from linten.integrations.vantage.vantage_logger import VantageLogger
from linten.integrations.vector_store_integrations.vector_store_pre_call_hook import (
    VectorStorePreCallHook,
)
from linten.integrations.zerobus import ZerobusLogger
from linten.proxy.hooks.dynamic_rate_limiter import (  # noqa: F401  # legacy module exports
    PROXY_DynamicRateLimitHandler,
    _PROXY_DynamicRateLimitHandler,  # pyright: ignore[reportPrivateUsage,reportUnusedImport]  # backwards-compatible package export
)
from linten.proxy.hooks.dynamic_rate_limiter_v3 import (  # noqa: F401  # legacy module exports
    PROXY_DynamicRateLimitHandlerV3,
    _PROXY_DynamicRateLimitHandlerV3,  # pyright: ignore[reportPrivateUsage,reportUnusedImport]  # backwards-compatible package export
)


class CustomLoggerRegistry:
    """
    Registry mapping the callback class string to the class type.
    """

    CALLBACK_CLASS_STR_TO_CLASS_TYPE = {
        "lago": LagoLogger,
        "openmeter": OpenMeterLogger,
        "braintrust": BraintrustLogger,
        "galileo": GalileoObserve,
        "langsmith": LangsmithLogger,
        "literalai": LiteralAILogger,
        "linten_agent": LintenAgentModelResolver,
        "prometheus": PrometheusLogger,
        "datadog": DataDogLogger,
        "datadog_llm_observability": DataDogLLMObsLogger,
        "datadog_metrics": DatadogMetricsLogger,
        "gcs_bucket": GCSBucketLogger,
        "opik": OpikLogger,
        "argilla": ArgillaLogger,
        "opentelemetry": OpenTelemetry,
        "azure_sentinel": AzureSentinelLogger,
        "azure_storage": AzureBlobStorageLogger,
        "humanloop": HumanloopLogger,
        # OTEL compatible loggers
        "logfire": OpenTelemetry,
        "arize": OpenTelemetry,
        "langfuse_otel": OpenTelemetry,
        "arize_phoenix": OpenTelemetry,
        "langtrace": OpenTelemetry,
        "weave_otel": OpenTelemetry,
        "levo": OpenTelemetry,
        "signoz": OpenTelemetry,
        "mlflow": MlflowLogger,
        "langfuse": LangfusePromptManagement,
        "otel": OpenTelemetry,
        "gcs_pubsub": GcsPubSubLogger,
        "anthropic_cache_control_hook": AnthropicCacheControlHook,
        "agentops": AgentOps,
        "deepeval": DeepEvalLogger,
        "s3_v2": S3Logger,
        "pointfive": PointFiveLogger,
        "zerobus": ZerobusLogger,
        "aws_sqs": SQSLogger,
        "dynamic_rate_limiter": PROXY_DynamicRateLimitHandler,
        "dynamic_rate_limiter_v3": PROXY_DynamicRateLimitHandlerV3,
        "vector_store_pre_call_hook": VectorStorePreCallHook,
        "dotprompt": DotpromptManager,
        "bitbucket": BitBucketPromptManager,
        "gitlab": GitLabPromptManager,
        "cloudzero": CloudZeroLogger,
        "focus": FocusLogger,
        "mavvrik": MavvrikFocusLogger,
        "vantage": VantageLogger,
        "ternary": TernaryLogger,
        "posthog": PostHogLogger,
        "newrelic": NewRelicLogger,
    }

    try:
        from linten_enterprise.enterprise_callbacks.pagerduty.pagerduty import (
            PagerDutyAlerting,
        )
        from linten_enterprise.enterprise_callbacks.send_emails.resend_email import (
            ResendEmailLogger,
        )
        from linten_enterprise.enterprise_callbacks.send_emails.sendgrid_email import (
            SendGridEmailLogger,
        )
        from linten_enterprise.enterprise_callbacks.send_emails.smtp_email import (
            SMTPEmailLogger,
        )

        from linten.integrations.generic_api.generic_api_callback import (
            GenericAPILogger,
        )

        enterprise_loggers = {
            "pagerduty": PagerDutyAlerting,
            "generic_api": GenericAPILogger,
            "resend_email": ResendEmailLogger,
            "sendgrid_email": SendGridEmailLogger,
            "smtp_email": SMTPEmailLogger,
        }
        CALLBACK_CLASS_STR_TO_CLASS_TYPE.update(enterprise_loggers)
    except ImportError:
        pass  # enterprise not installed

    @classmethod
    def get_callback_str_from_class_type(cls, class_type: type) -> str | None:
        """
        Get the callback string from the class type.

        Args:
            class_type: The class type to find the string for

        Returns:
            str: The callback string, or None if not found
        """
        for (
            callback_str,
            callback_class,
        ) in cls.CALLBACK_CLASS_STR_TO_CLASS_TYPE.items():
            if callback_class == class_type:
                return callback_str
        return None

    @classmethod
    def get_all_callback_strs_from_class_type(cls, class_type: type) -> list[str]:
        """
        Get all callback strings that map to the same class type.
        Some class types (like OpenTelemetry) have multiple string mappings.

        Args:
            class_type: The class type to find all strings for

        Returns:
            list: List of callback strings that map to the class type
        """
        callback_strs: Final[list[str]] = []
        for (
            callback_str,
            callback_class,
        ) in cls.CALLBACK_CLASS_STR_TO_CLASS_TYPE.items():
            if callback_class == class_type:
                callback_strs.append(callback_str)
        return callback_strs

    @classmethod
    def get_class_type_for_custom_logger_name(
        cls,
        custom_logger_name: _custom_logger_compatible_callbacks_literal,
    ) -> type:
        """
        Get the class type for a given custom logger name
        """
        return cls.CALLBACK_CLASS_STR_TO_CLASS_TYPE[custom_logger_name]
