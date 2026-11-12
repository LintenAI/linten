"""
Test that all standard HTTP error exceptions are exported from linten.__init__.
"""

import linten


def test_permission_denied_error_is_exported():
    """PermissionDeniedError (403) should be accessible as linten.PermissionDeniedError."""
    assert hasattr(linten, "PermissionDeniedError")
    assert linten.PermissionDeniedError is not None


def test_all_http_error_exceptions_exported():
    """All standard HTTP error exceptions should be accessible at module level."""
    expected_exceptions = [
        "BadRequestError",  # 400
        "AuthenticationError",  # 401
        "PermissionDeniedError",  # 403
        "NotFoundError",  # 404
        "Timeout",  # 408
        "UnprocessableEntityError",  # 422
        "RateLimitError",  # 429
        "InternalServerError",  # 500
        "BadGatewayError",  # 502
        "ServiceUnavailableError",  # 503
    ]
    for exc_name in expected_exceptions:
        assert hasattr(
            linten, exc_name
        ), f"linten.{exc_name} is not exported from linten.__init__"
