import pytest


@pytest.mark.asyncio
async def test_claude_code_plugin_table_schema_exists():

    with open("schema.prisma", "r") as f:
        schema = f.read()
    assert "Linten_ClaudeCodePluginTable" in schema, (
        "Linten_ClaudeCodePluginTable model missing from schema.prisma - "
        "this causes AttributeError on all /claude-code/plugins endpoints"
    )

    with open("linten/proxy/schema.prisma", "r") as f:
        proxy_schema = f.read()
    assert (
        "Linten_ClaudeCodePluginTable" in proxy_schema
    ), "Linten_ClaudeCodePluginTable model missing from linten/proxy/schema.prisma"
