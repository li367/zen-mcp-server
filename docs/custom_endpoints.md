# Custom Endpoints for Model Providers

Zen MCP Server supports configuring custom API endpoints for each model provider. This allows you to:

- Use private or regional API endpoints for official providers
- Connect to self-hosted model deployments
- Use compatible third-party API services
- Configure different endpoints for different models from the same provider

## Configuration Methods

You can configure custom endpoints in two ways:

### 1. Environment Variables

Use environment variables with the following format:
```
PROVIDER_MODELNAME_ENDPOINT=https://custom-endpoint.com
PROVIDER_MODELNAME_API_KEY=your-custom-api-key
```

Where:
- `PROVIDER` is the provider type (OPENAI, GOOGLE, XAI, DIAL)
- `MODELNAME` is the model name (with hyphens replaced by underscores)
- `ENDPOINT` is the suffix for the endpoint URL
- `API_KEY` is the suffix for the API key (optional)

Examples:
```
# Custom OpenAI endpoint for O3 model
OPENAI_O3_ENDPOINT=https://custom-openai-endpoint.com/v1
OPENAI_O3_API_KEY=your-custom-api-key

# Custom Gemini endpoint for Gemini 2.5 Pro model
GOOGLE_GEMINI25PRO_ENDPOINT=https://custom-gemini-endpoint.com
GOOGLE_GEMINI25PRO_API_KEY=your-custom-api-key

# Custom X.AI endpoint for Grok model
XAI_GROK_ENDPOINT=https://custom-xai-endpoint.com/v1
XAI_GROK_API_KEY=your-custom-api-key

# Custom DIAL endpoint for a specific model
DIAL_O3_ENDPOINT=https://custom-dial-endpoint.com/openai
DIAL_O3_API_KEY=your-custom-api-key
```

### 2. Configuration Files

You can also use JSON configuration files to define multiple endpoints:

```
OPENAI_ENDPOINTS_CONFIG=/path/to/openai_endpoints.json
GOOGLE_ENDPOINTS_CONFIG=/path/to/google_endpoints.json
XAI_ENDPOINTS_CONFIG=/path/to/xai_endpoints.json
DIAL_ENDPOINTS_CONFIG=/path/to/dial_endpoints.json
```

Example configuration file format:
```json
{
  "openai_endpoints": {
    "o3": {
      "base_url": "https://custom-openai-endpoint.com/v1",
      "api_key": "your-custom-api-key"
    },
    "o4-mini": {
      "base_url": "https://another-openai-endpoint.com/v1",
      "api_key": "another-custom-api-key"
    }
  }
}
```

## Provider-Specific Notes

### OpenAI

- Base URL should include the `/v1` path
- Compatible with Azure OpenAI endpoints

### Google (Gemini)

- Uses the Google AI SDK's client_options for custom endpoints
- Base URL should be the API endpoint without any path

### X.AI (Grok)

- Base URL should include the `/v1` path
- Uses OpenAI-compatible API format

### DIAL

- Base URL should end with `/openai` for the OpenAI-compatible API
- Uses Azure OpenAI-style deployment endpoints

## Unified OpenAI Interface

For the unified OpenAI interface, you can still use the legacy format:
```
MODELNAME_ENDPOINT=https://custom-endpoint.com/v1
MODELNAME_API_KEY=your-custom-api-key
```

Example:
```
GPT4_ENDPOINT=https://my-custom-gpt-endpoint.com/v1
GPT4_API_KEY=your-custom-api-key
```

## Security Considerations

- API keys are sensitive information and should be protected
- Use environment variables or secure configuration files
- Do not commit API keys to version control
- Consider using a secrets manager for production deployments