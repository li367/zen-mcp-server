"""Example script demonstrating custom endpoints for model providers."""

import os
import sys
import logging
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from providers.openai_provider import OpenAIModelProvider
from providers.gemini import GeminiModelProvider
from providers.xai import XAIModelProvider
from providers.dial import DIALModelProvider

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def main():
    """Run example of custom endpoints for model providers."""
    # Set up custom endpoints for demonstration
    os.environ["OPENAI_O3_ENDPOINT"] = "https://custom-openai-endpoint.com/v1"
    os.environ["OPENAI_O3_API_KEY"] = "custom-openai-key"
    
    os.environ["GOOGLE_GEMINI25PRO_ENDPOINT"] = "https://custom-gemini-endpoint.com"
    os.environ["GOOGLE_GEMINI25PRO_API_KEY"] = "custom-gemini-key"
    
    os.environ["XAI_GROK_ENDPOINT"] = "https://custom-xai-endpoint.com/v1"
    os.environ["XAI_GROK_API_KEY"] = "custom-xai-key"
    
    os.environ["DIAL_O3_ENDPOINT"] = "https://custom-dial-endpoint.com/openai"
    os.environ["DIAL_O3_API_KEY"] = "custom-dial-key"
    
    # Get API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY", "default-openai-key")
    google_api_key = os.getenv("GOOGLE_API_KEY", "default-google-key")
    xai_api_key = os.getenv("XAI_API_KEY", "default-xai-key")
    dial_api_key = os.getenv("DIAL_API_KEY", "default-dial-key")
    
    # Create providers with default endpoints
    logger.info("Creating providers with default endpoints...")
    openai_provider = OpenAIModelProvider(openai_api_key)
    gemini_provider = GeminiModelProvider(google_api_key)
    xai_provider = XAIModelProvider(xai_api_key)
    dial_provider = DIALModelProvider(dial_api_key)
    
    # Create providers with custom endpoints
    logger.info("Creating providers with custom endpoints...")
    custom_openai = OpenAIModelProvider(openai_api_key, model_name="o3")
    custom_gemini = GeminiModelProvider(google_api_key, model_name="gemini-2.5-pro")
    custom_xai = XAIModelProvider(xai_api_key, model_name="grok")
    custom_dial = DIALModelProvider(dial_api_key, model_name="o3")
    
    # Log the endpoints being used
    logger.info("Default OpenAI endpoint: %s", openai_provider.client.base_url)
    logger.info("Custom OpenAI endpoint: %s", custom_openai.client.base_url)
    
    # Note: For Gemini, the endpoint is set when the client is initialized
    logger.info("Default Gemini endpoint: %s", "https://generativelanguage.googleapis.com")
    logger.info("Custom Gemini endpoint: %s", custom_gemini._custom_api_url)
    
    logger.info("Default X.AI endpoint: %s", xai_provider.client.base_url)
    logger.info("Custom X.AI endpoint: %s", custom_xai.client.base_url)
    
    logger.info("Default DIAL endpoint: %s", dial_provider.client.base_url)
    logger.info("Custom DIAL endpoint: %s", custom_dial.client.base_url)
    
    logger.info("Custom endpoints example completed successfully!")


if __name__ == "__main__":
    main()