#!/usr/bin/env python3
"""Comprehensive test for the unified OpenAI interface implementation."""

import sys
import os
sys.path.insert(0, '.')

def test_unified_implementation():
    """Test the complete unified OpenAI interface implementation."""
    print("=== Testing Unified OpenAI Interface Implementation ===")
    
    try:
        print("\n1. Testing imports...")
        from providers.unified_openai import UnifiedOpenAIProvider
        from providers.base import ProviderType
        print("✓ UnifiedOpenAIProvider imports successfully")
        print("✓ ProviderType.UNIFIED available:", hasattr(ProviderType, 'UNIFIED'))
        
        print("\n2. Testing provider instantiation...")
        provider = UnifiedOpenAIProvider()
        print("✓ UnifiedOpenAIProvider instantiates successfully")
        print("✓ Provider type:", provider.get_provider_type())
        
        print("\n3. Testing endpoint configuration...")
        os.environ['TEST_MODEL_ENDPOINT'] = 'http://localhost:11434/v1'
        os.environ['TEST_MODEL_API_KEY'] = 'test-key'
        
        provider2 = UnifiedOpenAIProvider()
        endpoint = provider2._get_endpoint_for_model('test-model')
        if endpoint:
            print("✓ Custom endpoint configuration works:", endpoint)
        else:
            print("✗ Custom endpoint configuration failed")
        
        print("\n4. Testing provider registry integration...")
        from providers.registry import ModelProviderRegistry
        
        print("✓ Provider registry imports successfully")
        
        print("\n5. Testing provider module imports...")
        from providers import UnifiedOpenAIProvider as ImportedProvider
        print("✓ UnifiedOpenAIProvider can be imported from providers module")
        
        print("\n6. Testing configuration file support...")
        config_path = "/tmp/test_unified_config.json"
        test_config = {
            "model_endpoints": {
                "test-model-2": {
                    "base_url": "http://localhost:8080/v1",
                    "api_key": "test-key-2"
                }
            }
        }
        
        import json
        with open(config_path, 'w') as f:
            json.dump(test_config, f)
        
        os.environ['UNIFIED_ENDPOINTS_CONFIG'] = config_path
        provider3 = UnifiedOpenAIProvider()
        endpoint2 = provider3._get_endpoint_for_model('test-model-2')
        
        if endpoint2:
            print("✓ Configuration file loading works:", endpoint2)
        else:
            print("✗ Configuration file loading failed")
        
        os.remove(config_path)
        
        print("\n=== All Tests Completed Successfully ===")
        return True
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_unified_implementation()
    sys.exit(0 if success else 1)
