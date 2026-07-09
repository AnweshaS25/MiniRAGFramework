from google import genai

import os

from src.llms.base_llm import BaseLLM
from src.core.llm_response import LLMResponse

from dotenv import load_dotenv


class GeminiLLM(BaseLLM):
    """
    Gemini implementation using Google's GenAI SDK.
    """

    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash", temperature: float = 0.7,):

        load_dotenv()

        api_key = api_key or os.getenv("GOOGLE_API_KEY")

        if api_key is None:
            raise ValueError(
                "Gemini API key not found. "
                "Please provide it or set GOOGLE_API_KEY in your .env file."
            )
        
        if not model.strip():
            raise ValueError(
                "model cannot be empty."
            )

        if not 0 <= temperature <= 1:
            raise ValueError(
                "temperature must be between 0 and 1."
            )

        self.model = model
        self.temperature = temperature

        self.client = genai.Client(
            api_key=api_key
        )

        self._context_window = 1048576

    @property
    def context_window(self) -> int:
        return self._context_window

    def generate(self, prompt: str, **kwargs,) -> LLMResponse:
        if not prompt.strip():
            raise ValueError("prompt cannot be empty.")

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "temperature": kwargs.get(
                        "temperature",
                        self.temperature,
                    ),
                },
            )

        except Exception as e:
            raise RuntimeError(
                f"Gemini generation failed: {e}"
            )

        return LLMResponse(
            text=response.text,
            model=self.model,
        )