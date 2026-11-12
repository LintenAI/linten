import importlib

import pytest


@pytest.fixture(scope="module", autouse=True)
def import_mcp_server_before_manager_doubles() -> None:
    importlib.import_module("linten.proxy.mcp_server.server")
