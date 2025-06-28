"""Unified OpenAI-compatible provider that can route to any model with custom endpoints."""

import logging
import os
from typing import Optional, Dict, Any

from .base import ModelProvider, ModelResponse, ProviderType, ModelCapabilities
from .registry import ModelProviderRegistry

logger = logging.getLogger(__name__)


class UnifiedOpenAIProvider(ModelProvider):
    """
    Unified OpenAI-compatible provider that can route requests to any model
    with customizable endpoints while maintaining OpenAI API compatibility.
    """
    
    FRIENDLY_NAME = "Unified OpenAI"
    
    def __init__(self, api_key: str = "", **kwargs):
        """Initialize the unified provider."""
        super().__init__(api_key=api_key)
        self._model_endpoints = self._load_model_endpoints()
        self._provider_cache = {}
    
    def _load_model_endpoints(self) -> Dict[str, Dict[str, str]]:
        """Load custom endpoints configuration for models."""
        endpoints = {}
        
        for key, value in os.environ.items():
            if key.endswith('_ENDPOINT'):
                model_name = key[:-9].lower().replace('_', '-')
                endpoints[model_name] = {
                    'base_url': value,
                    'api_key': os.getenv(f"{key[:-9]}_API_KEY", "")
                }
        
        config_path = os.getenv("UNIFIED_ENDPOINTS_CONFIG")
        if config_path:
            try:
                import json
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    endpoints.update(file_config.get('model_endpoints', {}))
            except Exception as e:
                logger.warning(f"Failed to load unified endpoints config: {e}")
        
        return endpoints
    
    def _get_endpoint_for_model(self, model_name: str) -> Optional[Dict[str, str]]:
        """Get custom endpoint configuration for a model."""
        if model_name in self._model_endpoints:
            return self._model_endpoints[model_name]
        
        model_lower = model_name.lower()
        for configured_model, config in self._model_endpoints.items():
            if configured_model.lower() == model_lower:
                return config
        
        return None
    
    def _get_underlying_provider(self, model_name: str) -> Optional[ModelProvider]:
        """Get the underlying provider for a model."""
        if model_name in self._provider_cache:
            return self._provider_cache[model_name]
        
        endpoint_config = self._get_endpoint_for_model(model_name)
        if endpoint_config:
            try:
                from .custom import CustomProvider
                provider = CustomProvider(
                    api_key=endpoint_config.get('api_key', ''),
                    base_url=endpoint_config['base_url']
                )
                self._provider_cache[model_name] = provider
                return provider
            except ImportError:
                logger.warning("CustomProvider not available, falling back to registry")
        
        provider = ModelProviderRegistry.get_provider_for_model(model_name)
        if provider:
            self._provider_cache[model_name] = provider
        
        return provider
    
    def generate_content(
        self,
        prompt: str,
        model_name: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = None,
        **kwargs,
    ) -> ModelResponse:
        """Generate content by routing to the appropriate provider."""
        provider = self._get_underlying_provider(model_name)
        
        if not provider:
            raise ValueError(f"No provider found for model: {model_name}")
        
        try:
            from .openai_compatible import OpenAICompatibleProvider
            if isinstance(provider, OpenAICompatibleProvider):
                return provider.generate_content(
                    prompt=prompt,
                    model_name=model_name,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    **kwargs
                )
        except ImportError:
            pass
        
        response = provider.generate_content(
            prompt=prompt,
            model_name=model_name,
            system_prompt=system_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            **kwargs
        )
        
        if hasattr(response, 'friendly_name'):
            response.friendly_name = self.FRIENDLY_NAME
        return response
    
    def get_capabilities(self, model_name: str) -> ModelCapabilities:
        """Get capabilities by delegating to the underlying provider."""
        provider = self._get_underlying_provider(model_name)
        if not provider:
            raise ValueError(f"No provider found for model: {model_name}")
        
        return provider.get_capabilities(model_name)
    
    def validate_model_name(self, model_name: str) -> bool:
        """Validate model by checking if any provider supports it."""
        if self._get_endpoint_for_model(model_name):
            return True
        
        provider = ModelProviderRegistry.get_provider_for_model(model_name)
        return provider is not None
    
    def get_provider_type(self) -> ProviderType:
        """Return a unified provider type for the unified provider."""
        return ProviderType.UNIFIED
    
    def supports_thinking_mode(self, model_name: str) -> bool:
        """Check thinking mode support by delegating to underlying provider."""
        provider = self._get_underlying_provider(model_name)
        if not provider:
            return False
        
        return provider.supports_thinking_mode(model_name)
    
    def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens by delegating to underlying provider."""
        provider = self._get_underlying_provider(model_name)
        if not provider:
            return len(text) // 4
        
        return provider.count_tokens(text, model_name)
