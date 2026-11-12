import importlib
import sys
from collections.abc import Mapping

import pytest

import linten.mcp_client
import linten.mcp_client.client
import linten.mcp_client.tools

OLD_PACKAGE = "linten.experimental_mcp_client"


def test_old_package_warns_and_deep_imports_resolve_to_mcp_client(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in tuple(sys.modules):
        if name.startswith(OLD_PACKAGE):
            monkeypatch.delitem(sys.modules, name)

    with pytest.warns(DeprecationWarning, match="linten.mcp_client"):
        import linten.experimental_mcp_client as old

    assert old.client is linten.mcp_client.client
    assert old.tools is linten.mcp_client.tools
    assert old.__all__ == linten.mcp_client.__all__
    assert old.load_mcp_tools is linten.mcp_client.load_mcp_tools
    assert old.call_openai_tool is linten.mcp_client.call_openai_tool
    assert importlib.import_module(f"{OLD_PACKAGE}.client") is linten.mcp_client.client
    assert importlib.import_module(f"{OLD_PACKAGE}.tools") is linten.mcp_client.tools
    attrs: Mapping[str, object] = vars(old)
    assert attrs["tools"] is linten.mcp_client.tools
    assert attrs["client"] is linten.mcp_client.client
