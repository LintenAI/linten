# Gollem Go Agent Framework with Linten

A working example showing how to use [gollem](https://github.com/fugue-labs/gollem), a production-grade Go agent framework, with Linten as a proxy gateway. This lets Go developers access 100+ LLM providers through a single proxy while keeping compile-time type safety for tools and structured output.

## Quick Start

### 1. Start Linten Proxy

```bash
# Simple start with a single model
linten --model gpt-4o

# Or with the example config for multi-provider access
linten --config proxy_config.yaml
```

### 2. Run the examples

```bash
# Install Go dependencies
go mod tidy

# Basic agent
go run ./basic

# Agent with type-safe tools
go run ./tools

# Streaming responses
go run ./streaming
```

## Configuration

The included `proxy_config.yaml` sets up three providers through Linten:

```yaml
model_list:
  - model_name: gpt-4o          # OpenAI
  - model_name: claude-sonnet    # Anthropic
  - model_name: gemini-pro       # Google Vertex AI
```

Switch providers in Go by changing a single string — no code changes needed:

```go
model := openai.NewLinten("http://localhost:4000",
    openai.WithModel("gpt-4o"),        // OpenAI
    // openai.WithModel("claude-sonnet"),  // Anthropic
    // openai.WithModel("gemini-pro"),     // Google
)
```

## Examples

### `basic/` — Basic Agent

Connects gollem to Linten and runs a simple prompt. Demonstrates the `NewLinten` constructor and basic agent creation.

### `tools/` — Type-Safe Tools

Shows gollem's compile-time type-safe tool framework working through Linten's tool-use passthrough. The tool parameters are Go structs with JSON tags — the schema is generated automatically at compile time.

### `streaming/` — Streaming Responses

Real-time token streaming using Go 1.23+ range-over-function iterators, proxied through Linten's SSE passthrough.

## How It Works

Gollem's `openai.NewLinten()` constructor creates an OpenAI-compatible provider pointed at your Linten proxy. Since Linten speaks the OpenAI API protocol, everything works out of the box:

- **Chat completions** — standard request/response
- **Tool use** — Linten passes tool definitions and calls through transparently
- **Streaming** — Server-Sent Events proxied through Linten
- **Structured output** — JSON schema response format works with supporting models

```
Go App (gollem) → Linten Proxy → OpenAI / Anthropic / Google / ...
```

## Why Use This?

- **Type-safe Go**: Compile-time type checking for tools, structured output, and agent configuration — no runtime surprises
- **Single proxy, many models**: Switch between OpenAI, Anthropic, Google, and 100+ other providers by changing a model name string
- **Zero-dependency core**: gollem's core has no external dependencies — just stdlib
- **Single binary deployment**: `go build` produces one binary, no pip/venv/Docker needed
- **Cost tracking & rate limiting**: Linten handles cost tracking, rate limits, and fallbacks at the proxy layer

## Environment Variables

```bash
# Required for providers you want to use (set in Linten config or env)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional: point to a non-default Linten proxy
export LINTEN_PROXY_URL="http://localhost:4000"
```

## Troubleshooting

**Connection errors?**
- Make sure Linten is running: `linten --model gpt-4o`
- Check the URL is correct (default: `http://localhost:4000`)

**Model not found?**
- Verify the model name matches what's configured in Linten
- Run `curl http://localhost:4000/models` to see available models

**Tool calls not working?**
- Ensure the underlying model supports tool use (GPT-4o, Claude, Gemini)
- Check Linten logs for any provider-specific errors

## Learn More

- [gollem GitHub](https://github.com/fugue-labs/gollem)
- [gollem API Reference](https://pkg.go.dev/github.com/fugue-labs/gollem/core)
- [Linten Proxy Docs](https://docs.linten.ai/docs/simple_proxy)
- [Linten Supported Models](https://docs.linten.ai/docs/providers)
