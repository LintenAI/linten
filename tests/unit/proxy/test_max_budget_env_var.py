"""
Test that max_budget from environment variable (string) is correctly
converted to float.
GitHub Issue: #23843
"""

from unittest.mock import patch

import pytest

import linten


@pytest.mark.asyncio
async def test_max_budget_string_converted_to_float():
    """
    When max_budget is set via os.environ/MAX_BUDGET, it arrives as a
    string. initialize() should convert it to float so the comparison
    `linten.max_budget > 0` doesn't raise TypeError.
    """
    with patch("linten.proxy.proxy_server.generate_feedback_box"):
        from linten.proxy.proxy_server import initialize

        original = linten.max_budget
        try:
            await initialize(max_budget="100.5")
            assert isinstance(linten.max_budget, float)
            assert linten.max_budget == 100.5
        finally:
            linten.max_budget = original


@pytest.mark.asyncio
async def test_max_budget_float_stays_float():
    """max_budget as float should still work."""
    with patch("linten.proxy.proxy_server.generate_feedback_box"):
        from linten.proxy.proxy_server import initialize

        original = linten.max_budget
        try:
            await initialize(max_budget=200.0)
            assert isinstance(linten.max_budget, float)
            assert linten.max_budget == 200.0
        finally:
            linten.max_budget = original
