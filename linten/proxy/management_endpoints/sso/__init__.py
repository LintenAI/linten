"""
SSO (Single Sign-On) related modules for Linten Proxy.

This package contains custom SSO implementations and utilities.
"""

from linten.proxy.management_endpoints.sso.custom_microsoft_sso import (
    CustomMicrosoftSSO,
)
from linten.proxy.management_endpoints.sso.linten_http_client_sso import (
    LintenGoogleSSO,
    LintenHttpClientSSO,
    create_generic_sso_provider,
)

__all__ = ["CustomMicrosoftSSO", "LintenGoogleSSO", "LintenHttpClientSSO", "create_generic_sso_provider"]
