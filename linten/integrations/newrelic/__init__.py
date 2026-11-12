"""
New Relic AI Monitoring Integration for Linten

This module provides integration with New Relic's AI Monitoring feature to track
LLM requests, responses, and usage metrics.
"""

from linten.integrations.newrelic.newrelic import NewRelicLogger

__all__ = ["NewRelicLogger"]
