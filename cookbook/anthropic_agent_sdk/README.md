# Claude Agent SDK with Linten Gateway

A simple example showing how to use Claude's Agent SDK with Linten as a proxy. This lets you use any LLM provider (OpenAI, Bedrock, Azure, etc.) through the Agent SDK.

## Quick Start

### 1. Install dependencies

```bash
pip install anthropic claude-agent-sdk linten
```

### 2. Start Linten proxy

```bash
# Simple start with Claude
linten --model claude-sonnet-4-20250514

# Or with a config file
linten --config config.yaml
```

Generate a master key before starting the proxy:

```bash
export LINTEN_MASTER_KEY="sk-$(openssl rand -hex 32)"
```

### 3. Run the chat

**Basic Agent (no MCP):**

```bash
python main.py
```

**Agent with MCP (DeepWiki2 for research):**

```bash
python agent_with_mcp.py
```

If MCP connection fails, you can disable it:

```bash
USE_MCP=false python agent_with_mcp.py
```

That's it! You can now chat with the agent in your terminal.

### Chat Commands

While chatting, you can use these commands:
- `models` - List all available models (fetched from your Linten proxy)
- `model` - Switch to a different model
- `clear` - Start a new conversation
- `quit` or `exit` - End the chat

The chat automatically fetches available models from your Linten proxy's `/models` endpoint, so you'll always see what's currently configured.

## Configuration

Set these environment variables if needed:

```bash
export LINTEN_PROXY_URL="http://localhost:4000"
export LINTEN_API_KEY="$LINTEN_MASTER_KEY"
export LINTEN_MODEL="bedrock-claude-sonnet-4.5"
```

Or just use the defaults - it'll connect to `http://localhost:4000` by default.

## Files

- `main.py` - Basic interactive agent without MCP
- `agent_with_mcp.py` - Agent with MCP server integration (DeepWiki2)
- `common.py` - Shared utilities and functions
- `config.example.yaml` - Example Linten configuration
- `requirements.txt` - Python dependencies

## Example Config File

If you want to use multiple models, create a `config.yaml` (see `config.example.yaml`):

```yaml
model_list:
  - model_name: bedrock-claude-sonnet-4
    linten_params:
      model: "bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0"
      aws_region_name: "us-east-1"

  - model_name: bedrock-claude-sonnet-4.5
    linten_params:
      model: "bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
      aws_region_name: "us-east-1"
```

Then start Linten with: `linten --config config.yaml`

## How It Works

The key is pointing the Agent SDK to Linten instead of directly to Anthropic:

```python
# Point to Linten gateway (not Anthropic)
os.environ["ANTHROPIC_BASE_URL"] = "http://localhost:4000"
os.environ["ANTHROPIC_API_KEY"] = os.environ["LINTEN_API_KEY"]

# Use any model configured in Linten
options = ClaudeAgentOptions(
    model="bedrock-claude-sonnet-4",  # or gpt-4, or anything else
    system_prompt="You are a helpful assistant.",
    max_turns=50,
)
```

Note: Don't add `/anthropic` to the base URL - Linten handles the routing automatically.

## Why Use This?

- **Switch providers easily**: Use the same code with OpenAI, Bedrock, Azure, etc.
- **Cost tracking**: Linten tracks spending across all your agent conversations
- **Rate limiting**: Set budgets and limits on your agent usage
- **Load balancing**: Distribute requests across multiple API keys or regions
- **Fallbacks**: Automatically retry with a different model if one fails

## Troubleshooting

**Connection errors?**
- Make sure Linten is running: `linten --model your-model`
- Check the URL is correct (default: `http://localhost:4000`)

**Authentication errors?**
- Verify your Linten API key is correct
- Make sure the model is configured in your Linten setup

**Model not found?**
- Check the model name matches what's in your Linten config
- Run `linten --model your-model` to test it works

**Agent with MCP stuck or failing?**
- The MCP server might not be available at `http://localhost:4000/mcp/deepwiki2`
- Try disabling MCP: `USE_MCP=false python agent_with_mcp.py`
- Or use the basic agent: `python main.py`

## Learn More

- [Linten Docs](https://docs.linten.ai/)
- [Claude Agent SDK](https://github.com/anthropics/anthropic-agent-sdk)
- [Linten Proxy Guide](https://docs.linten.ai/docs/proxy/quick_start)
