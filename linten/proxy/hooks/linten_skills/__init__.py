"""
Linten Skills Hook - Proxy integration for skills

This module provides the CustomLogger hook for skills processing.
The actual skill logic is in linten/llms/linten_proxy/skills/.

Usage:
    from linten.proxy.hooks.linten_skills import SkillsInjectionHook

    # Register hook in proxy
    linten.callbacks.append(SkillsInjectionHook())
"""

# Re-export from the SDK location for convenience
from linten.llms.linten_proxy.skills import (
    LINTEN_CODE_EXECUTION_TOOL,
    CodeExecutionHandler,
    LintenInternalTools,
    SkillPromptInjectionHandler,
    SkillsSandboxExecutor,
    code_execution_handler,
    get_linten_code_execution_tool,
)
from linten.proxy.hooks.linten_skills.main import SkillsInjectionHook

__all__ = [
    "LINTEN_CODE_EXECUTION_TOOL",
    "CodeExecutionHandler",
    "LintenInternalTools",
    "SkillPromptInjectionHandler",
    "SkillsInjectionHook",
    "SkillsSandboxExecutor",
    "code_execution_handler",
    "get_linten_code_execution_tool",
]
