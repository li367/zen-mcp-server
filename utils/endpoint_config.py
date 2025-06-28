"""Endpoint configuration utilities for model providers."""

import logging
import os
import json
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

class EndpointConfig:
    """Configuration for custom API endpoints."""
    
    def __init__(self, provider_type: str):
        """Initialize endpoint configuration for a specific provider.
        
        Args:
            provider_type: The provider type (e.g., 'google', 'openai', 'xai')
        """
        self.provider_type = provider_type.lower()
        self._endpoints = self._load_endpoints()
    
    def _load_endpoints(self) -> Dict[str, Dict[str, str]]:
        """Load custom endpoint configurations for this provider.
        
        Returns:
            Dictionary mapping model names to endpoint configurations
        """
        endpoints = {}
        
        # Load from environment variables
        # Format: PROVIDER_MODELNAME_ENDPOINT and PROVIDER_MODELNAME_API_KEY
        # Example: GOOGLE_GEMINI_ENDPOINT, OPENAI_GPT4_ENDPOINT
        prefix = f"{self.provider_type.upper()}_"
        suffix = "_ENDPOINT"
        
        for key, value in os.environ.items():
            if key.startswith(prefix) and key.endswith(suffix):
                # Extract model name from environment variable
                # GOOGLE_GEMINI25PRO_ENDPOINT -> gemini-2.5-pro
                model_part = key[len(prefix):-len(suffix)]
                # Convert GEMINI25PRO to gemini-2-5-pro format
                model_name = model_part.lower()
                # Replace underscores with dashes
                model_name = model_name.replace('_', '-')
                
                # Log the model name for debugging
                logger.debug(f"Extracted model name from environment variable: {model_name}")
                
                # Get corresponding API key if available
                api_key_var = f"{prefix}{model_part}_API_KEY"
                api_key = os.getenv(api_key_var, "")
                
                endpoints[model_name] = {
                    'base_url': value,
                    'api_key': api_key
                }
                logger.info(f"Loaded custom endpoint for {self.provider_type} model '{model_name}'")
        
        # Load from configuration file if specified
        config_path = os.getenv(f"{self.provider_type.upper()}_ENDPOINTS_CONFIG")
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    provider_endpoints = file_config.get(f'{self.provider_type}_endpoints', {})
                    endpoints.update(provider_endpoints)
                    logger.info(f"Loaded {len(provider_endpoints)} custom endpoints for {self.provider_type} from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load {self.provider_type} endpoints config: {e}")
        
        return endpoints
    
    def get_endpoint_for_model(self, model_name: str) -> Optional[Dict[str, str]]:
        """Get custom endpoint configuration for a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary with 'base_url' and 'api_key' if found, None otherwise
        """
        # Normalize model name for comparison
        normalized_name = self._normalize_model_name(model_name)
        
        # Direct match
        if normalized_name in self._endpoints:
            return self._endpoints[normalized_name]
        
        # Try case-insensitive match
        normalized_lower = normalized_name.lower()
        for configured_model, config in self._endpoints.items():
            if configured_model.lower() == normalized_lower:
                return config
            
            # Try with different dash/underscore patterns
            configured_lower = configured_model.lower()
            if configured_lower.replace('-', '') == normalized_lower.replace('-', ''):
                return config
        
        return None
        
    def _normalize_model_name(self, model_name: str) -> str:
        """Normalize model name for consistent comparison.
        
        Args:
            model_name: Original model name
            
        Returns:
            Normalized model name
        """
        # Convert to lowercase
        name = model_name.lower()
        
        # Replace underscores with dashes
        name = name.replace('_', '-')
        
        # Remove any special characters
        name = ''.join(c for c in name if c.isalnum() or c == '-')
        
        return name
    
    def has_custom_endpoint(self, model_name: str) -> bool:
        """Check if a model has a custom endpoint configuration.
        
        Args:
            model_name: Name of the model
            
        Returns:
            True if a custom endpoint is configured, False otherwise
        """
        result = self.get_endpoint_for_model(model_name) is not None
        if result:
            logger.debug(f"Found custom endpoint for {self.provider_type} model '{model_name}'")
        return result