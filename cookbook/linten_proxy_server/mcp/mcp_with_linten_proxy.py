"""
Use Linten Proxy MCP Gateway to call MCP tools.

When using Linten Proxy, you can use the same MCP tools across all your LLM providers.
"""

import os

import openai

client = openai.OpenAI(
    api_key=os.environ["LINTEN_MASTER_KEY"],
    base_url="http://localhost:4000",  # paste your linten proxy base url here
)
print("Making API request to Responses API with MCP tools")

response = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": "give me TLDR of what LintenAI/linten repo is about",
            "type": "message",
        }
    ],
    tools=[
        {
            "type": "mcp",
            "server_label": "linten",
            "server_url": "linten_proxy",
            "require_approval": "never",
        }
    ],
    stream=True,
    tool_choice="required",
)

for chunk in response:
    print("response chunk: ", chunk)
