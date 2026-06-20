from typing import Optional
import os

from dotenv import load_dotenv
from groq import Groq

from src.core.llm_response import LLMResponse
from src.llms.base_llm import BaseLLM

class GroqLLM(BaseLLM):
    """
    Groq implementation of the BaseLLM interface.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.2, max_tokens: int = 1024,):

        if not (0 <= temperature <= 2):
            raise ValueError("temperature must be between 0 and 2.")

        if max_tokens <= 0:
            raise ValueError("max_tokens must be greater than 0.")
        
        load_dotenv()

        api_key = api_key or os.getenv("GROQ_API_KEY")

        if api_key is None:
            raise ValueError("Groq API key not found. Please provide it or set GROQ_API_KEY in your .env file.")
        
        self._api_key = api_key
        
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens


        self._client = Groq(api_key=api_key)


    def generate(self, prompt: str,) -> LLMResponse:

        if not prompt or not prompt.strip():
            raise ValueError("prompt cannot be empty.")
        
        try:
            response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=self.temperature,
            max_completion_tokens=self.max_tokens,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate response from Groq: {e}") from e

        text = response.choices[0].message.content

        usage = response.usage

        return LLMResponse(
            text=text,
            model=self.model_name,
            prompt_tokens=usage.prompt_tokens if usage else None,
            completion_tokens=usage.completion_tokens if usage else None,
            total_tokens=usage.total_tokens if usage else None,
        )
    
    