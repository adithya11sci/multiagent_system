
import os
import logging
from typing import Dict, Any, Optional

from config import GEMINI_API_KEY, GROQ_API_KEY, LLM_PROVIDER
logger = logging.getLogger(__name__)

class LLMClient:
    """
    Unified client for interacting with different LLM providers (Gemini, Groq)
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = LLM_PROVIDER
        self.model_name = config.get("model")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1000)
        
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the appropriate client based on provider"""
        try:
            if self.provider == "groq":
                from groq import Groq
                if not GROQ_API_KEY:
                    raise ValueError("Groq API Key not found")
                self.client = Groq(api_key=GROQ_API_KEY)
                logger.info(f"Initialized Groq client with model {self.model_name}")
                
            elif self.provider == "gemini":
                import google.generativeai as genai
                if not GEMINI_API_KEY:
                    raise ValueError("Gemini API Key not found")
                genai.configure(api_key=GEMINI_API_KEY)
                self.client = genai.GenerativeModel(self.model_name)
                logger.info(f"Initialized Gemini client with model {self.model_name}")
                
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            self.client = None

    def generate_content(self, prompt: str) -> Any:
        """
        Generate content from the LLM
        Returns an object with a .text attribute to match Gemini's interface
        """
        if not self.client:
            raise RuntimeError("LLM Client not initialized")
            
        if self.provider == "groq":
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                
                # Wrap response to match Gemini's interface
                class ResponseWrapper:
                    def __init__(self, text):
                        self.text = text
                        
                return ResponseWrapper(completion.choices[0].message.content)
                
            except Exception as e:
                logger.error(f"Groq API error: {e}")
                raise e
                
        elif self.provider == "gemini":
            return self.client.generate_content(prompt)
            
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
