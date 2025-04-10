from openai import OpenAI
from .config import Config
from .logger import Logger

class LLMClient:
    """Client for interacting with the LLM model."""
    
    def __init__(self):
        """Initialize the LLM client."""
        self.logger = Logger(name="llm_client")
        self.logger.info(f"Initializing LLM client with model: {Config.OPENAI_MODEL}")
        
        # Initialize OpenAI client
        self.client = OpenAI(**Config.get_ollama_client_kwargs())
        self.model = Config.OPENAI_MODEL
    
    def generate_text(self, prompt, system_prompt="You are a helpful assistant.", max_tokens=2000, temperature=0.7):
        """Generate text based on the given prompt."""
        try:
            self.logger.debug(f"Generating text with prompt: {prompt[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error generating text: {str(e)}")
            return f"Error: {str(e)}"
    
    def generate_with_history(self, conversation_history, max_tokens=2000, temperature=0.7):
        """Generate text based on conversation history."""
        try:
            self.logger.debug(f"Generating text with conversation history of {len(conversation_history)} messages")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation_history,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error generating text with history: {str(e)}")
            return f"Error: {str(e)}"
