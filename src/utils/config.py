import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration handler for the slow agent."""
    
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "llama4")
    
    # Agent configuration
    PATIENCE_LEVEL = os.getenv("PATIENCE_LEVEL", "high")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))
    TIMEOUT = int(os.getenv("TIMEOUT", "120"))
    
    @classmethod
    def get_ollama_client_kwargs(cls):
        """Get the kwargs for initializing the OpenAI client for Ollama."""
        return {
            "api_key": cls.OPENAI_API_KEY if cls.OPENAI_API_KEY else "ollama",
            "base_url": cls.OPENAI_API_BASE,
        }
