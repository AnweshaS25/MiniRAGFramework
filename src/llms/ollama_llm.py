from ollama import Client

from src.core.llm_response import LLMResponse
from src.llms.base_llm import BaseLLM

class OllamaLLM(BaseLLM):
    """
    Large Language Model implementation using Ollama.
    """

    def __init__(self, model: str = "llama3.2", host: str = "http://localhost:11434",temperature: float = 0.7,):

        if not model.strip():
            raise ValueError("model cannot be empty.")

        if not host.strip():
            raise ValueError("host cannot be empty.")

        if not 0 <= temperature <= 1:
            raise ValueError(
                "temperature must be between 0 and 1."
            )
        
        self.model = model
        self.host = host
        self.temperature = temperature

        self.client = Client(host=self.host)


    def generate(self, prompt: str, **kwargs,) -> LLMResponse:
        """
        Generate a response using Ollama.
        """

        if not prompt.strip():
            raise ValueError("prompt cannot be empty.")

        temperature = kwargs.get(
            "temperature",
            self.temperature,
        )

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                options={
                    "temperature": temperature,
                },
            )

        except Exception as e:
            raise RuntimeError(
                f"Failed to generate response using Ollama: {e}"
            )
        

        return LLMResponse(
            text=response.message.content,
            model=response.model,
            prompt_tokens=response.prompt_eval_count,
            completion_tokens=response.eval_count,
            total_tokens=(
                response.prompt_eval_count
                + response.eval_count
            ),
        )