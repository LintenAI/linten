import linten.mcp_client as _mcp_client
from linten.linten_core_utils.deprecated_package import alias_deprecated_package
from linten.mcp_client import call_openai_tool, load_mcp_tools

alias_deprecated_package(__name__, _mcp_client)

__all__ = ["call_openai_tool", "load_mcp_tools"]
