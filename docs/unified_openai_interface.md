# Unified OpenAI-Compatible Interface

The Zen MCP Server now supports a unified OpenAI-compatible interface that allows you to use any model through a consistent API while supporting custom endpoints.

## Features

- **Universal Model Access**: Use any supported model through OpenAI-compatible API calls
- **Custom Endpoints**: Configure custom API endpoints for specific models
- **Backward Compatibility**: All existing functionality continues to work unchanged
- **Smart Routing**: Automatically routes requests to the appropriate underlying provider
- **Flexible Configuration**: Support for both environment variables and JSON configuration files

## Configuration

### Environment Variables

Enable the unified interface and configure custom endpoints:

```bash
# Enable unified OpenAI interface
ENABLE_UNIFIED_OPENAI=true

# Configure custom endpoints for specific models
# Format: MODELNAME_ENDPOINT and MODELNAME_API_KEY
LLAMA3_2_ENDPOINT=http://localhost:11434/v1
LLAMA3_2_API_KEY=

# Example for a custom GPT endpoint
GPT4_ENDPOINT=https://my-custom-openai-endpoint.com/v1
GPT4_API_KEY=your-custom-api-key
```

### Configuration File

Alternatively, use a JSON configuration file:

```bash
# Set path to configuration file
UNIFIED_ENDPOINTS_CONFIG=/path/to/unified_endpoints.json
```

Example configuration file (`unified_endpoints.json`):

```json
{
  "model_endpoints": {
    "llama3.2": {
      "base_url": "http://localhost:11434/v1",
      "api_key": ""
    },
    "gpt-4": {
      "base_url": "https://my-custom-openai-endpoint.com/v1",
      "api_key": "your-custom-api-key"
    },
    "claude-3": {
      "base_url": "https://my-anthropic-proxy.com/v1",
      "api_key": "your-proxy-api-key"
    }
  }
}
```

## How It Works

1. **Provider Registration**: When `ENABLE_UNIFIED_OPENAI=true`, the unified provider is registered with the highest priority
2. **Endpoint Resolution**: For each model request, the system checks for custom endpoint configuration
3. **Smart Routing**: If a custom endpoint is found, requests are routed there; otherwise, they go to the appropriate native provider
4. **OpenAI Compatibility**: All responses maintain OpenAI-compatible format regardless of the underlying provider

## Use Cases

- **Local Development**: Route models to local inference servers (Ollama, vLLM, LM Studio)
- **Custom Deployments**: Use your own hosted model endpoints
- **Proxy Services**: Route through custom proxy services for enhanced security or monitoring
- **Multi-Provider Setup**: Mix and match different providers while maintaining a consistent interface

## Example Usage

With the unified interface enabled, you can use any model through standard OpenAI-compatible calls:

```python
# All these calls work the same way, regardless of the underlying provider
response = client.chat.completions.create(
    model="llama3.2",  # Routes to custom endpoint
    messages=[{"role": "user", "content": "Hello"}]
)

response = client.chat.completions.create(
    model="gemini-pro",  # Routes to native Gemini provider
    messages=[{"role": "user", "content": "Hello"}]
)

response = client.chat.completions.create(
    model="gpt-4",  # Routes to custom OpenAI endpoint if configured
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Priority Order

The unified provider has the highest priority in the provider resolution order:

1. **Unified Provider** (if enabled) - Checks for custom endpoints first
2. **Native Providers** (Google, OpenAI, X.AI, DIAL) - Direct API access
3. **Custom Provider** - Local/self-hosted models
4. **OpenRouter** - Catch-all for cloud models

This ensures that custom endpoint configurations take precedence while maintaining fallback to native providers.
