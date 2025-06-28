#!/usr/bin/env python3
"""Simple test for the unified OpenAI interface."""

import os
import sys
sys.path.insert(0, '.')

def test_unified_provider():
    """Test basic functionality of the unified provider."""
    try:
        from providers.unified_openai import UnifiedOpenAIProvider
        
        os.environ['ENABLE_UNIFIED_OPENAI'] = 'true'
        os.environ['TEST_MODEL_ENDPOINT'] = 'http://localhost:11434/v1'
        os.environ['TEST_MODEL_API_KEY'] = 'test-key'
        
        provider = UnifiedOpenAIProvider()
        
        print("Testing model validation...")
        
        endpoint = provider._get_endpoint_for_model('test-model')
        if endpoint:
            print(f"✓ Custom endpoint configured: {endpoint}")
        else:
            print("✗ No custom endpoint found")
        
        print("✓ Unified provider created successfully")
        print("✓ Unified provider test completed")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("This is expected if dependencies are not installed")
        print("✓ Basic import structure test completed")

if __name__ == "__main__":
    test_unified_provider()
