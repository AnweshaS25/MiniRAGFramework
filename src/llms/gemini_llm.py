from google import genai

from src.llms.base_llm import BaseLLM
from src.core.llm_response import LLMResponse


class GeminiLLM(BaseLLM):
    """
    Gemini implementation using Google's GenAI SDK.
    """

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", temperature: float = 0.7,):

        if not api_key:
            raise ValueError(
                "Gemini API key cannot be empty."
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