from abc import ABC, abstractmethod
from src.core.llm_response import LLMResponse

class BaseLLM(ABC):
    """
    Abstract base class for all Large Language Models.
    """

    @abstractmethod
    def generate(self, prompt: str,) -> LLMResponse:
        """
        Generate a response for the given prompt.
        """
        pass