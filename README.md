<h1 align="center">
        🚅 Linten
    </h1>
    <p align="center">
        <p align="center">Linten AI Gateway
        </p>
        <p align="center">Open Source AI Gateway for 100+ LLMs. Self-hosted. Enterprise-ready. Call any LLM in OpenAI format.</p>
        <p align="center">
        <a href="https://render.com/deploy?repo=https://github.com/LintenAI/linten" target="_blank" rel="nofollow"><img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" height="40"></a>
        <a href="https://railway.com/deploy/RhvhdC?referralCode=7mRv9K&utm_medium=integration&utm_source=template&utm_campaign=generic"><img src="https://railway.com/button.svg" alt="Deploy on Railway" height="40"></a>
        <a href="https://console.aws.amazon.com/cloudshell/home" target="_blank" rel="nofollow"><img src="./.github/deploy-on-aws.png" alt="Deploy on AWS" height="40"></a>
        <a href="https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2FLintenAI%2Fterraform-google-linten&cloudshell_git_branch=v1.105.0&cloudshell_workspace=examples%2Fdefault&cloudshell_tutorial=TUTORIAL.md&cloudshell_image=gcr.io/ds-artifacts-cloudshell/deploystack_custom_image&shellonly=true" target="_blank" rel="nofollow"><img src="./.github/deploy-on-gcp.png" alt="Deploy on GCP" height="40"></a>
        </p>
    </p>
<h4 align="center"><a href="https://docs.linten.ai/docs/simple_proxy" target="_blank">Linten Proxy Server (AI Gateway)</a> | <a href="https://docs.linten.ai/docs/enterprise#hosted-linten-proxy" target="_blank"> Hosted Proxy</a> | <a href="https://linten.ai/enterprise"target="_blank">Enterprise Tier</a> | <a href="https://www.linten.ai/ai-gateway" target="_blank">Website</a></h4>
<h4 align="center">
    <a href="https://pypi.org/project/linten/" target="_blank">
        <img src="https://img.shields.io/pypi/v/linten.svg" alt="PyPI Version">
    </a>
    <a href="https://github.com/LintenAI/linten" target="_blank">
        <img src="https://img.shields.io/github/stars/LintenAI/linten.svg?style=social" alt="GitHub Stars">
    </a>
    <a href="https://www.ycombinator.com/companies/lintenai">
        <img src="https://img.shields.io/badge/Y%20Combinator-W23-orange?style=flat-square" alt="Y Combinator W23">
    </a>
    <a href="https://wa.link/huol9n">
        <img src="https://img.shields.io/static/v1?label=Chat%20on&message=WhatsApp&color=success&logo=WhatsApp&style=flat-square" alt="Whatsapp">
    </a>
    <a href="https://discord.gg/wuPM9dRgDw">
        <img src="https://img.shields.io/static/v1?label=Chat%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
    <a href="https://www.linten.ai/support">
        <img src="https://img.shields.io/static/v1?label=Chat%20on&message=Slack&color=black&logo=Slack&style=flat-square" alt="Slack">
    </a>
    <a href="https://codspeed.io/LintenAI/linten?utm_source=badge">
        <img src="https://img.shields.io/endpoint?url=https://codspeed.io/badge.json" alt="CodSpeed"/>
    </a>
</h4>

<img alt="Linten AI Gateway" src=".github/assets/linten-gateway.png" />

---

## What is Linten

Linten is an open source AI Gateway that gives you a single, unified interface to call 100+ LLM providers — OpenAI, Anthropic, Gemini, Bedrock, Azure, and more — using the OpenAI format.

Use it as a **Python SDK** for direct library integration, or deploy the **AI Gateway (Proxy Server)** as a centralized service for your team or organization.

[**Jump to Linten Proxy (LLM Gateway) Docs**](https://docs.linten.ai/docs/simple_proxy) <br>
[**Jump to Supported LLM Providers**](https://docs.linten.ai/docs/providers)

---

## Why Linten

Managing LLM calls across providers gets complicated fast — different SDKs, auth patterns, request formats, and error types for every model. Linten removes that friction:

- **Unified API** — one interface for 100+ LLMs, no provider-specific SDK juggling
- **Drop-in OpenAI compatibility** — swap providers without rewriting your code
- **Production-ready gateway** — virtual keys, spend tracking, guardrails, load balancing, and an admin dashboard out of the box
- **8ms P95 latency** at 1k RPS ([benchmarks](https://docs.linten.ai/docs/benchmarks))

### OSS Adopters

<table>
  <tr>
    <td><img height="60" alt="Stripe" src="https://github.com/user-attachments/assets/f7296d4f-9fbd-460d-9d05-e4df31697c4b" /></td>
    <td><img height="60" alt="image" src="https://github.com/user-attachments/assets/436fca71-988b-40bb-b5fe-8450c80fdbd0" /></td>
    <td><img height="60" alt="Google ADK" src="https://github.com/user-attachments/assets/caf270a2-5aee-45c4-8222-41a2070c4f19" /></td>
    <td><img height="60" alt="Greptile" src="https://github.com/user-attachments/assets/3db0ae72-0843-4005-a56d-bba1dde2193d" /></td>
    <td><img height="60" alt="OpenHands" src="https://github.com/user-attachments/assets/a6150c4c-149e-4cae-888b-8b92be6e003f" /></td>
    <td><h2>Netflix</h2></td>
    <td><img height="60" alt="OpenAI Agents SDK" src="https://github.com/user-attachments/assets/c02f7be0-8c2e-4d27-aea7-7c024bfaebc0" /></td>
  </tr>
</table>

---

## Features

<details open>
<summary><b>LLMs</b> - Call 100+ LLMs (Python SDK + AI Gateway)</summary>

[**All Supported Endpoints**](https://docs.linten.ai/docs/supported_endpoints) - `/chat/completions`, `/responses`, `/embeddings`, `/images`, `/audio`, `/batches`, `/rerank`, `/a2a`, `/messages` and more.

### Python SDK

```shell
uv add linten
```

An independent `linten-core` distribution provides the Python SDK with the same
`import linten` API and runtime dependencies. It has no optional extras, CLI entry
points, or bundled dashboard. Install one SDK distribution per environment because
`linten` and `linten-core` own overlapping Python files. Use `linten` for the
proxy, CLI, and optional extras

Build and install core from this checkout while its release integration is pending:

```shell
python scripts/build_core_distribution.py --out-dir dist/core
python -m pip install dist/core/linten_core-*.whl
```

The builder requires Git, `uv` and the Rust build toolchain. It reads the release version
from the root `pyproject.toml`, leaves source files unchanged, and produces a wheel
and a self-contained sdist in `dist/core`. Run installation in a fresh environment
without `linten`

```python
from linten import completion
import os

os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

# OpenAI
response = completion(model="openai/gpt-4o", messages=[{"role": "user", "content": "Hello!"}])

# Anthropic  
response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[{"role": "user", "content": "Hello!"}])
```

### AI Gateway (Proxy Server)

[**Getting Started - E2E Tutorial**](https://docs.linten.ai/docs/proxy/docker_quick_start) - Setup virtual keys, make your first request

```shell
uv tool install 'linten[proxy]'
linten --model gpt-4o
```

```python
import openai

client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

</details>

<details>
<summary><b>Auto Routing</b> - Choose a model for each prompt (Python SDK + AI Gateway)</summary>

### Python SDK

[**Docs: Autorouter SDK**](https://docs.linten.ai/docs/autorouter_sdk)

Install with `uv add linten` and set `OPENAI_API_KEY` for the models below.

```python
import asyncio
from linten import Router

router = Router(model_list=[
    {"model_name": "fast", "linten_params": {"model": "openai/gpt-6-luna"}},
    {"model_name": "capable", "linten_params": {"model": "openai/gpt-6.1-sol"}},
    {"model_name": "auto", "linten_params": {
        "model": "auto_router/complexity_router",
        "complexity_router_config": {
            "classifier_type": "heuristic",
            "tiers": {"SIMPLE": "fast", "MEDIUM": "fast",
                      "COMPLEX": "capable", "REASONING": "capable"},
            "return_raw_model_name": True,
        },
        "complexity_router_default_model": "capable",
    }},
])
response = asyncio.run(router.acompletion(
    model="auto", messages=[{"role": "user", "content": "What is 2+2?"}],
))
print(response.model, response.choices[0].message.content)
```

### AI Gateway (Proxy Server)

[**Create an Auto Router**](https://docs.linten.ai/docs/auto_router/setup), then call its model name. Replace `auto` and the URL below with yours, and set `LINTEN_API_KEY` to your virtual key.

```shell
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LINTEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"What is 2+2?"}]}'
```

</details>

<details>
<summary><b>A2A</b> - Invoke A2A Agents (Python SDK + AI Gateway)</summary>

[**Supported Providers**](https://docs.linten.ai/docs/a2a#add-a2a-agents) - LangGraph, Vertex AI Agent Engine, Azure AI Foundry, Bedrock AgentCore, Pydantic AI

### Python SDK - A2A Protocol

```python
from linten.a2a_protocol import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams
from uuid import uuid4

client = A2AClient(base_url="http://localhost:10001")

request = SendMessageRequest(
    id=str(uuid4()),
    params=MessageSendParams(
        message={
            "role": "user",
            "parts": [{"kind": "text", "text": "Hello!"}],
            "messageId": uuid4().hex,
        }
    )
)
response = await client.send_message(request)
```

### AI Gateway (Proxy Server)

**Step 1.** [Add your Agent to the AI Gateway](https://docs.linten.ai/docs/a2a#adding-your-agent) — set `protocolVersion` to `1.0` or `0.3` per agent

**Step 2.** Call Agent via A2A SDK (requires `a2a-sdk>=1.1.0`)

```python
import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, SendMessageRequest
from a2a.utils.constants import TransportProtocol
from uuid import uuid4

base_url = "http://localhost:4000/a2a/my-agent"  # Linten proxy + agent name
headers = {"Authorization": "Bearer <your-master-key>"}    # Linten master key or a virtual key

async with httpx.AsyncClient(headers=headers, timeout=60.0) as http_client:
    resolver = A2ACardResolver(httpx_client=http_client, base_url=base_url)
    agent_card = await resolver.get_agent_card()
    config = ClientConfig(
        httpx_client=http_client,
        streaming=False,
        supported_protocol_bindings=[TransportProtocol.JSONRPC, TransportProtocol.HTTP_JSON],
    )
    client = ClientFactory(config).create(agent_card)

    request = SendMessageRequest(
        message=Message(
            message_id=uuid4().hex,
            role=Role.ROLE_USER,
            parts=[Part(text="Hello!")],
        )
    )
    async for event in client.send_message(request):
        populated = event.ListFields()
        if populated and populated[0][0].name in ("message", "msg"):
            print("".join(getattr(p, "text", "") or "" for p in populated[0][1].parts))
```

[**Docs: A2A Agent Gateway**](https://docs.linten.ai/docs/a2a)

</details>

<details>
<summary><b>MCP Tools</b> - Connect MCP servers to any LLM (Python SDK + AI Gateway)</summary>

### Python SDK - MCP Bridge

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from linten import mcp_client
import linten

server_params = StdioServerParameters(command="python", args=["mcp_server.py"])

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # Load MCP tools in OpenAI format
        tools = await mcp_client.load_mcp_tools(session=session, format="openai")

        # Use with any Linten model
        response = await linten.acompletion(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's 3 + 5?"}],
            tools=tools
        )
```

### AI Gateway - MCP Gateway

**Step 1.** [Add your MCP Server to the AI Gateway](https://docs.linten.ai/docs/mcp#adding-your-mcp)

**Step 2.** Call MCP tools via `/chat/completions`

```bash
curl -X POST 'http://0.0.0.0:4000/v1/chat/completions' \
  -H 'Authorization: Bearer <your-master-key>' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Summarize the latest open PR"}],
    "tools": [{
      "type": "mcp",
      "server_url": "linten_proxy/mcp/github",
      "server_label": "github_mcp",
      "require_approval": "never"
    }]
  }'
```

### Use with Cursor IDE

```json
{
  "mcpServers": {
    "Linten": {
      "url": "http://localhost:4000/mcp/",
      "headers": {
        "x-linten-api-key": "Bearer <your-master-key>"
      }
    }
  }
}
```

For MCP OAuth, an upstream may advertise dynamic client registration but refuse requests with HTTP 401 or 403. If the provider requires a pre-registered OAuth app, configure its `credentials.client_id` and, when required, `credentials.client_secret` on the MCP server. This skips dynamic registration in the gateway sign-in flow. The provider must approve the app for MCP access; reaching its authorization page does not establish that login or tool calls will succeed

[**Docs: MCP Gateway**](https://docs.linten.ai/docs/mcp)

</details>

<details>
<summary><b>Agents</b> - Run Claude Code, Codex, OpenCode, pi or Deep Agents on any model (Python SDK)</summary>

### Python SDK - Agents

```python
import linten
from linten import Harness, sandbox

result = linten.agent(
    Harness.CLAUDE_CODE,  # or Harness.CODEX, Harness.OPENCODE, Harness.PI, Harness.DEEPAGENTS
    "Find why tests/test_router.py is flaky and fix it.",
    sandbox=sandbox.local("./repo"),
    model="linten_proxy/claude-sonnet-4-5",  # a model group on your AI Gateway
)

print(result.text, result.cost, [f.path for f in result.files])
```

Set `LINTEN_PROXY_API_BASE` and `LINTEN_PROXY_API_KEY` and every model call the agent makes goes through your AI Gateway, tagged `harness,claude_code`. Drop the `linten_proxy/` prefix to call a provider directly. Install `starlette uvicorn` plus the agent's CLI (`claude`, `codex`, `opencode` or `pi`), or `deepagents langchain-linten` for Deep Agents.

[**Docs: Agent Harnesses**](https://docs.linten.ai/docs/harness)

</details>

### Supported Providers ([Website Supported Models](https://models.linten.ai/) | [Docs](https://docs.linten.ai/docs/providers))

| Provider                                                                            | `/chat/completions` | `/messages` | `/responses` | `/embeddings` | `/image/generations` | `/audio/transcriptions` | `/audio/speech` | `/moderations` | `/batches` | `/rerank` |
|-------------------------------------------------------------------------------------|---------------------|-------------|--------------|---------------|----------------------|-------------------------|-----------------|----------------|-----------|-----------|
| [Abliteration (`abliteration`)](https://docs.linten.ai/docs/providers/abliteration) | ✅ |  |  |  |  |  |  |  |  |  |
| [AI/ML API (`aiml`)](https://docs.linten.ai/docs/providers/aiml) | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |
| [AI21 (`ai21`)](https://docs.linten.ai/docs/providers/ai21) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [AI21 Chat (`ai21_chat`)](https://docs.linten.ai/docs/providers/ai21) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Aleph Alpha](https://docs.linten.ai/docs/providers/aleph_alpha) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Amazon Nova](https://docs.linten.ai/docs/providers/amazon_nova) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Anthropic (`anthropic`)](https://docs.linten.ai/docs/providers/anthropic) | ✅ | ✅ | ✅ |  |  |  |  |  | ✅ |  |
| [Anthropic Text (`anthropic_text`)](https://docs.linten.ai/docs/providers/anthropic) | ✅ | ✅ | ✅ |  |  |  |  |  | ✅ |  |
| [Anyscale](https://docs.linten.ai/docs/providers/anyscale) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [AssemblyAI (`assemblyai`)](https://docs.linten.ai/docs/pass_through/assembly_ai) | ✅ | ✅ | ✅ |  |  | ✅ |  |  |  |  |
| [Auto Router (`auto_router`)](https://docs.linten.ai/docs/proxy/auto_routing) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [AWS - Bedrock (`bedrock`)](https://docs.linten.ai/docs/providers/bedrock) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  | ✅ |
| [AWS - Sagemaker (`sagemaker`)](https://docs.linten.ai/docs/providers/aws_sagemaker) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |
| [Azure (`azure`)](https://docs.linten.ai/docs/providers/azure) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| [Azure AI (`azure_ai`)](https://docs.linten.ai/docs/providers/azure_ai) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| [Azure Text (`azure_text`)](https://docs.linten.ai/docs/providers/azure) | ✅ | ✅ | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |
| [Baseten (`baseten`)](https://docs.linten.ai/docs/providers/baseten) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Bytez (`bytez`)](https://docs.linten.ai/docs/providers/bytez) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Cerebras (`cerebras`)](https://docs.linten.ai/docs/providers/cerebras) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Clarifai (`clarifai`)](https://docs.linten.ai/docs/providers/clarifai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [CLF AI Gateway (`clf_ai_gateway`)](https://docs.linten.ai/docs/providers/clf_ai_gateway) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Cloudflare AI Workers (`cloudflare`)](https://docs.linten.ai/docs/providers/cloudflare_workers) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Codestral (`codestral`)](https://docs.linten.ai/docs/providers/codestral) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Cognition (`cognition`)](https://docs.linten.ai/docs/providers/cognition) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Cohere (`cohere`)](https://docs.linten.ai/docs/providers/cohere) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  | ✅ |
| [Cohere Chat (`cohere_chat`)](https://docs.linten.ai/docs/providers/cohere) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [CometAPI (`cometapi`)](https://docs.linten.ai/docs/providers/cometapi) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |
| [CompactifAI (`compactifai`)](https://docs.linten.ai/docs/providers/compactifai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [CoralBricks (`coralbricks`)](https://docs.linten.ai/docs/providers/coralbricks) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Custom (`custom`)](https://docs.linten.ai/docs/providers/custom_llm_server) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Custom OpenAI (`custom_openai`)](https://docs.linten.ai/docs/providers/openai_compatible) | ✅ | ✅ | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |
| [Dashscope (`dashscope`)](https://docs.linten.ai/docs/providers/dashscope) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  | ✅ |
| [Databricks (`databricks`)](https://docs.linten.ai/docs/providers/databricks) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [DataRobot (`datarobot`)](https://docs.linten.ai/docs/providers/datarobot) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Deepgram (`deepgram`)](https://docs.linten.ai/docs/providers/deepgram) | ✅ | ✅ | ✅ |  |  | ✅ |  |  |  |  |
| [DeepInfra (`deepinfra`)](https://docs.linten.ai/docs/providers/deepinfra) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Deepseek (`deepseek`)](https://docs.linten.ai/docs/providers/deepseek) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Eden AI (`edenai`)](https://docs.linten.ai/docs/providers/edenai) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  |
| [ElevenLabs (`elevenlabs`)](https://docs.linten.ai/docs/providers/elevenlabs) | ✅ | ✅ | ✅ |  |  | ✅ | ✅ |  |  |  |
| [EmpirioLabs AI (`empiriolabs`)](https://docs.linten.ai/docs/providers/empiriolabs) | ✅ |  | ✅ |  |  |  |  |  |  |  |
| [Empower (`empower`)](https://docs.linten.ai/docs/providers/empower) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [eu/jev Decisions API (`eu_jev`)](https://docs.linten.ai/docs/pass_through/eu_jev) |  |  |  |  |  |  |  |  |  |  |
| [Fal AI (`fal_ai`)](https://docs.linten.ai/docs/providers/fal_ai) | ✅ | ✅ | ✅ |  | ✅ |  |  |  |  |  |
| [Featherless AI (`featherless_ai`)](https://docs.linten.ai/docs/providers/featherless_ai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Fireworks AI (`fireworks_ai`)](https://docs.linten.ai/docs/providers/fireworks_ai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [FriendliAI (`friendliai`)](https://docs.linten.ai/docs/providers/friendliai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Galadriel (`galadriel`)](https://docs.linten.ai/docs/providers/galadriel) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [GitHub Copilot (`github_copilot`)](https://docs.linten.ai/docs/providers/github_copilot) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |
| [GitHub Models (`github`)](https://docs.linten.ai/docs/providers/github) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Google - PaLM](https://docs.linten.ai/docs/providers/palm) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Google - Vertex AI (`vertex_ai`)](https://docs.linten.ai/docs/providers/vertex) | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |
| [Google AI Studio - Gemini (`gemini`)](https://docs.linten.ai/docs/providers/gemini) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [GradientAI (`gradient_ai`)](https://docs.linten.ai/docs/providers/gradient_ai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Groq AI (`groq`)](https://docs.linten.ai/docs/providers/groq) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Heroku (`heroku`)](https://docs.linten.ai/docs/providers/heroku) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Hosted VLLM (`hosted_vllm`)](https://docs.linten.ai/docs/providers/vllm) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Huggingface (`huggingface`)](https://docs.linten.ai/docs/providers/huggingface) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  | ✅ |
| [Hyperbolic (`hyperbolic`)](https://docs.linten.ai/docs/providers/hyperbolic) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [IBM - Watsonx.ai (`watsonx`)](https://docs.linten.ai/docs/providers/watsonx) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |
| [Infinity (`infinity`)](https://docs.linten.ai/docs/providers/infinity) |  |  |  | ✅ |  |  |  |  |  |  |
| [Jina AI (`jina_ai`)](https://docs.linten.ai/docs/providers/jina_ai) |  |  |  | ✅ |  |  |  |  |  |  |
| [Lambda AI (`lambda_ai`)](https://docs.linten.ai/docs/providers/lambda_ai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Lemonade (`lemonade`)](https://docs.linten.ai/docs/providers/lemonade) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Linten Proxy (`linten_proxy`)](https://docs.linten.ai/docs/providers/linten_proxy) | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |
| [Llamafile (`llamafile`)](https://docs.linten.ai/docs/providers/llamafile) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [LM Studio (`lm_studio`)](https://docs.linten.ai/docs/providers/lm_studio) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Maritalk (`maritalk`)](https://docs.linten.ai/docs/providers/maritalk) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Meta - Llama API (`meta_llama`)](https://docs.linten.ai/docs/providers/meta_llama) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Mistral AI API (`mistral`)](https://docs.linten.ai/docs/providers/mistral) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |
| [ModelScope (`modelscope`)](https://docs.linten.ai/docs/providers/modelscope) | ✅ | ✅ | ✅ |  | ✅ |  |  |  |  |  |
| [Moonshot (`moonshot`)](https://docs.linten.ai/docs/providers/moonshot) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Morph (`morph`)](https://docs.linten.ai/docs/providers/morph) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Nace (`nace`)](https://console.nace.ai/docs/drex) |  |  |  |  |  |  |  |  |  |  |
| [Nebius AI Studio (`nebius`)](https://docs.linten.ai/docs/providers/nebius) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |
| [NLP Cloud (`nlp_cloud`)](https://docs.linten.ai/docs/providers/nlp_cloud) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Novita AI (`novita`)](https://novita.ai/models/llm?utm_source=github_linten&utm_medium=github_readme&utm_campaign=github_link) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Nscale (`nscale`)](https://docs.linten.ai/docs/providers/nscale) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Nvidia NIM (`nvidia_nim`)](https://docs.linten.ai/docs/providers/nvidia_nim) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [OCI (`oci`)](https://docs.linten.ai/docs/providers/oci) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Ollama (`ollama`)](https://docs.linten.ai/docs/providers/ollama) | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |
| [Ollama Chat (`ollama_chat`)](https://docs.linten.ai/docs/providers/ollama) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Oobabooga (`oobabooga`)](https://docs.linten.ai/docs/providers/openai_compatible) | ✅ | ✅ | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |
| [OpenAI (`openai`)](https://docs.linten.ai/docs/providers/openai) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| [OpenAI-like (`openai_like`)](https://docs.linten.ai/docs/providers/openai_compatible) |  |  |  | ✅ |  |  |  |  |  |  |
| [OpenRouter (`openrouter`)](https://docs.linten.ai/docs/providers/openrouter) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [OVHCloud AI Endpoints (`ovhcloud`)](https://docs.linten.ai/docs/providers/ovhcloud) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Parallel AI (`parallel_ai`)](https://docs.linten.ai/docs/search/parallel_ai) |  |  |  |  |  |  |  |  |  |  |
| [Perplexity AI (`perplexity`)](https://docs.linten.ai/docs/providers/perplexity) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Petals (`petals`)](https://docs.linten.ai/docs/providers/petals) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Pinstripes (`pinstripes`)](https://docs.linten.ai/docs/providers/pinstripes) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Predibase (`predibase`)](https://docs.linten.ai/docs/providers/predibase) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Qianwen AI Platform (`qwen_ai_platform`)](https://docs.linten.ai/docs/providers/qwencloud) | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  |  | ✅ |
| [QwenCloud (`qwencloud`)](https://docs.linten.ai/docs/providers/qwencloud) | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  |  | ✅ |
| [Recraft (`recraft`)](https://docs.linten.ai/docs/providers/recraft) |  |  |  |  | ✅ |  |  |  |  |  |
| [Replicate (`replicate`)](https://docs.linten.ai/docs/providers/replicate) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Sagemaker Chat (`sagemaker_chat`)](https://docs.linten.ai/docs/providers/aws_sagemaker) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Sail (`sail`)](https://docs.linten.ai/docs/providers/sail) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Sambanova (`sambanova`)](https://docs.linten.ai/docs/providers/sambanova) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [ScaleDown (`scaledown`)](https://docs.linten.ai/docs/providers/scaledown) | ✅ |  |  |  |  |  |  |  |  |  |
| [Snowflake (`snowflake`)](https://docs.linten.ai/docs/providers/snowflake) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Strands Decider (`strands_decider`)](https://docs.linten.ai/docs/providers) |  |  |  |  |  |  |  |  |  |  |
| [Text Completion Codestral (`text-completion-codestral`)](https://docs.linten.ai/docs/providers/codestral) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Text Completion OpenAI (`text-completion-openai`)](https://docs.linten.ai/docs/providers/text_completion_openai) | ✅ | ✅ | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |
| [Together AI (`together_ai`)](https://docs.linten.ai/docs/providers/togetherai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Topaz (`topaz`)](https://docs.linten.ai/docs/providers/topaz) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Triton (`triton`)](https://docs.linten.ai/docs/providers/triton-inference-server) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Typesafe Decisions API (`typesafe`)](https://docs.linten.ai/docs/providers) |  |  |  |  |  |  |  |  |  |  |
| [V0 (`v0`)](https://docs.linten.ai/docs/providers/v0) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Vercel AI Gateway (`vercel_ai_gateway`)](https://docs.linten.ai/docs/providers/vercel_ai_gateway) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [VLLM (`vllm`)](https://docs.linten.ai/docs/providers/vllm) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Volcengine (`volcengine`)](https://docs.linten.ai/docs/providers/volcano) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [VoyageAI by MongoDB (`voyage`)](https://docs.linten.ai/docs/providers/voyage) |  |  |  | ✅ |  |  |  |  |  |  |
| [WandB Inference (`wandb`)](https://docs.linten.ai/docs/providers/wandb_inference) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Watsonx Text (`watsonx_text`)](https://docs.linten.ai/docs/providers/watsonx) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [xAI (`xai`)](https://docs.linten.ai/docs/providers/xai) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |
| [Xinference (`xinference`)](https://docs.linten.ai/docs/providers/xinference) |  |  |  | ✅ |  |  |  |  |  |  |
| [ZeroGPU (`zerogpu`)](https://docs.linten.ai/docs/providers/zerogpu) | ✅ | ✅ | ✅ |  |  |  |  |  |  |  |

[**Read the Docs**](https://docs.linten.ai/docs/)

---

## Get Started

You can use Linten through either the Proxy Server or Python SDK. Both give you a unified interface to access multiple LLMs (100+ LLMs). Choose the option that best fits your needs:

<table style={{width: '100%', tableLayout: 'fixed'}}>
<thead>
<tr>
<th style={{width: '14%'}}></th>
<th style={{width: '43%'}}><strong><a href="https://docs.linten.ai/docs/simple_proxy">Linten AI Gateway</a></strong></th>
<th style={{width: '43%'}}><strong><a href="https://docs.linten.ai/docs/python_sdk">Linten Python SDK</a></strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style={{width: '14%'}}><strong>Use Case</strong></td>
<td style={{width: '43%'}}>Central service (LLM Gateway) to access multiple LLMs</td>
<td style={{width: '43%'}}>Use Linten directly in your Python code</td>
</tr>
<tr>
<td style={{width: '14%'}}><strong>Who Uses It?</strong></td>
<td style={{width: '43%'}}>Gen AI Enablement / ML Platform Teams</td>
<td style={{width: '43%'}}>Developers building LLM projects</td>
</tr>
<tr>
<td style={{width: '14%'}}><strong>Key Features</strong></td>
<td style={{width: '43%'}}>Centralized API gateway with authentication and authorization, multi-tenant cost tracking and spend management per project/user, per-project customization (logging, guardrails, caching), virtual keys for secure access control, admin dashboard UI for monitoring and management</td>
<td style={{width: '43%'}}>Direct Python library integration in your codebase, Router with retry/fallback logic across multiple deployments (e.g. Azure/OpenAI) - <a href="https://docs.linten.ai/docs/routing">Router</a>, application-level load balancing and cost tracking, exception handling with OpenAI-compatible errors, observability callbacks (Lunary, MLflow, Langfuse, etc.)</td>
</tr>
</tbody>
</table>

**Stable Release:** Use docker images with the `-stable` tag. These have undergone 12 hour load tests, before being published. [More information about the release cycle here](https://docs.linten.ai/docs/proxy/release_cycle)

Support for more providers. Missing a provider or LLM Platform, raise a [feature request](https://github.com/LintenAI/linten/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.yml&title=%5BFeature%5D%3A+).

### Deploy on AWS or GCP with Terraform

Run the Linten proxy as a production-ready componentized stack (gateway, backend, UI on separate services; managed Postgres + Redis + object store) using the published Terraform modules. Both modules are on the [public Terraform Registry](https://registry.terraform.io/namespaces/LintenAI) — no auth needed.

#### AWS — ECS Fargate + Aurora + ElastiCache + ALB

[![Launch in AWS CloudShell](https://img.shields.io/badge/Launch-AWS_CloudShell-FF9900?logo=amazon-aws&logoColor=white)](https://console.aws.amazon.com/cloudshell/home) — opens an in-browser shell, already authenticated to your AWS account. Once inside, run:

```bash
git clone https://github.com/LintenAI/linten.git
cd linten/terraform/linten/aws/examples/default
cp terraform.tfvars.example terraform.tfvars   # edit region/tenant/env
terraform init && terraform apply
```

[Module page →](https://registry.terraform.io/modules/LintenAI/linten/aws/latest)

Or call the module from your own root config:

```hcl
# main.tf
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.60" }
  }
}

provider "aws" {
  region = "us-west-2"
}

module "linten" {
  source  = "LintenAI/linten/aws"
  version = "~> 1.89"

  region = "us-west-2"
  azs    = ["us-west-2a", "us-west-2b"]
  tenant = "acme"
  env    = "prod"

  # Production: provide an ACM cert. Without one, set allow_plaintext_alb = true
  # (dev/trial only).
  # acm_certificate_arn = "arn:aws:acm:us-west-2:111122223333:certificate/..."
  allow_plaintext_alb = true
}

output "linten_url" {
  value = module.linten.alb_dns_name
}
```

```bash
terraform init
terraform apply
```

Provider API keys live in AWS Secrets Manager; reference ARNs via `gateway_extra_secrets`. Full input list and architecture diagram on the [registry page](https://registry.terraform.io/modules/LintenAI/linten/aws/latest?tab=inputs).

#### GCP — Cloud Run + Cloud SQL + Memorystore + HTTPS LB

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2FLintenAI%2Fterraform-google-linten&cloudshell_git_branch=v1.105.0&cloudshell_workspace=examples%2Fdefault&cloudshell_tutorial=TUTORIAL.md&cloudshell_image=gcr.io/ds-artifacts-cloudshell/deploystack_custom_image&shellonly=true)

Real 1-click. Opens Cloud Shell, clones the [terraform-google-linten](https://github.com/LintenAI/terraform-google-linten) module mirror at the latest stable release (a small download instead of the full linten repo), and walks you through `terraform apply` via a built-in [DeployStack tutorial](./terraform/linten/gcp/examples/default/TUTORIAL.md). Pick the project, the tutorial sets up the Artifact Registry remote repo, writes `terraform.tfvars` from your answers, and runs apply

[Module page →](https://registry.terraform.io/modules/LintenAI/linten/google/latest)

To call the module from your own config instead, Cloud Run can't pull from `ghcr.io` directly, so first set up a one-time Artifact Registry remote repo backed by GHCR:

```bash
gcloud artifacts repositories create linten \
  --location=us-central1 \
  --repository-format=docker \
  --mode=remote-repository \
  --remote-docker-repo=https://ghcr.io \
  --project=my-gcp-project
```

Then:

```hcl
# main.tf
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google      = { source = "hashicorp/google",      version = "~> 6.10" }
    google-beta = { source = "hashicorp/google-beta", version = "~> 6.10" }
  }
}

provider "google"      { project = "my-gcp-project"; region = "us-central1" }
provider "google-beta" { project = "my-gcp-project"; region = "us-central1" }

module "linten" {
  source  = "LintenAI/linten/google"
  version = "~> 1.89"

  project_id = "my-gcp-project"
  region     = "us-central1"
  tenant     = "acme"
  env        = "prod"

  # Replace my-gcp-project with your GCP project ID (same value as project_id above).
  image_registry = "us-central1-docker.pkg.dev/my-gcp-project/linten/lintenai"

  # Production: provide DNS already pointing at the LB IP for Google-managed certs.
  # Without one, set allow_plaintext_lb = true (dev/trial only).
  # lb_domains         = ["proxy.example.com"]
  allow_plaintext_lb = true
}

output "linten_url" {
  value = module.linten.load_balancer_url
}
```

```bash
terraform init
terraform apply
```

Provider API keys live in Secret Manager; reference resource IDs (e.g. `projects/my-gcp-project/secrets/openai-api-key`) via `gateway_extra_secrets`. Full input list and architecture diagram on the [registry page](https://registry.terraform.io/modules/LintenAI/linten/google/latest?tab=inputs).

#### Both stacks include

- The full componentized split (gateway / backend / UI as independent services)
- Managed Postgres (writer + reader) and Redis
- Versioned object store for proxy state + file uploads
- An auto-generated `LINTEN_MASTER_KEY` in your cloud's secret manager
- A one-off migration job that runs `prisma migrate deploy` before the proxy starts
- The same `proxy_config` surface as the [Helm chart](./helm/linten/) — pass YAML as a typed map

The Terraform modules live at [`terraform/linten/aws/`](./terraform/linten/aws/) and [`terraform/linten/gcp/`](./terraform/linten/gcp/) in this repo; the registry entries are read-only mirrors updated on each release.

### Run in Developer Mode
#### Services
1. Setup .env file in root
2. Run dependent services `docker-compose up db prometheus`

#### Backend
1. Run `make bootstrap`
2. Start proxy backend: `uv run python linten/proxy/proxy_cli.py`

#### Frontend
1. Navigate to `ui/linten-dashboard` (dependencies were already installed w/ `make bootstrap`)
2. Start dashboard: `npm run dev`

### Verify Docker Image Signatures

All Linten Docker images published to GHCR are signed with [cosign](https://docs.sigstore.dev/cosign/overview/). Releases are signed with the key introduced in [commit `e82a3c6`](https://github.com/LintenAI/linten/commit/e82a3c646908ba0a6ee0beddc4310d7a6cac4065).

**Verify using the pinned commit hash (recommended):**

A commit hash is cryptographically immutable, so this is the strongest way to ensure you are using the published signing key:

```bash
cosign verify \
  --key https://raw.githubusercontent.com/LintenAI/linten/e82a3c646908ba0a6ee0beddc4310d7a6cac4065/cosign.pub \
  ghcr.io/lintenai/linten:<release-tag>
```

**Verify using a release tag (convenience):**

Tags are protected in this repository and resolve to the same key. This option is easier to read but relies on tag protection rules:

```bash
cosign verify \
  --key https://raw.githubusercontent.com/LintenAI/linten/<release-tag>/cosign.pub \
  ghcr.io/lintenai/linten:<release-tag>
```

Replace `<release-tag>` with the version you are deploying (e.g. `v1.83.0-stable`).

---

# Enterprise
For companies that need better security, user management and professional support

[Get an Enterprise License](https://linten.ai/enterprise)
[Talk to founders](https://enterprise.linten.ai/demo)

This covers:
- ✅ **Features under the [Linten Commercial License](https://docs.linten.ai/docs/enterprise):**
- ✅ **Feature Prioritization**
- ✅ **Custom Integrations**
- ✅ **Professional Support - Dedicated discord + slack**
- ✅ **Custom SLAs**
- ✅ **Secure access with Single Sign-On**

# Contributing

We welcome contributions to Linten! Whether you're fixing bugs, adding features, or improving documentation, we appreciate your help.

If you want to work closely with our team, check out [Linten OSS Champions](https://www.linten.ai/champions), our program for trusted OSS contributors with their own Slack channel and a voice in the roadmap

## Quick Start for Contributors

This requires uv to be installed.

```bash
git clone https://github.com/LintenAI/linten.git
cd linten
make install-dev    # Install development dependencies
make format         # Format your code
make lint           # Run all linting checks
make test-unit      # Run unit tests
make format-check   # Check formatting only
```

For detailed contributing guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

> **📖 Contributing to documentation?** The Linten docs have moved to a separate repository: [LintenAI/linten-docs](https://github.com/LintenAI/linten-docs). Please open doc PRs there. Docs are served at [docs.linten.ai](https://docs.linten.ai).

## Code Quality / Linting

Linten follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

Our automated checks include:
- **Ruff** for formatting, linting, and code quality
- **basedpyright** for type checking
- **Circular import detection**
- **Import safety checks**


All these checks must pass before your PR can be merged.


# Support / talk with founders

- [Schedule Demo 👋](https://calendly.com/d/4mp-gd3-k5k/lintenai-1-1-onboarding-linten-hosted-version)
- [Community Discord 💭](https://discord.gg/wuPM9dRgDw)
- [Community Slack 💭](https://www.linten.ai/support)
- Our email ✉️ agents@linten.ai

# Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<a href="https://github.com/LintenAI/linten/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=LintenAI/linten" />
</a>
