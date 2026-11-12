"""
Proxy Authentication module for Linten SDK.

This module provides OAuth2/JWT token management for authenticating
with Linten Proxy or any OAuth2-protected endpoint.

Usage:
    from linten.proxy_auth import AzureADCredential, ProxyAuthHandler

    linten.proxy_auth = ProxyAuthHandler(
        credential=AzureADCredential(),
        scope="api://my-proxy/.default"
    )
"""

from .credentials import (
    AccessToken,
    AzureADCredential,
    GenericOAuth2Credential,
    ProxyAuthHandler,
    TokenCredential,
)

__all__ = [
    "AccessToken",
    "AzureADCredential",
    "GenericOAuth2Credential",
    "ProxyAuthHandler",
    "TokenCredential",
]
