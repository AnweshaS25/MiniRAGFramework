from abc import ABC, abstractmethod
from src.core.llm_response import LLMResponse
from src.core.llm_metadata import LLMMetadata

class BaseLLM(ABC):
    """
    Abstract base class for all Large Language Models.
    """

    @property
    @abstractmethod
    def context_window(self) -> int:
        """
        Maximum context window supported by the model.
        """
        pass

    @property
    @abstractmethod
    def metadata(self) -> LLMMetadata:
        """
        Metadata describing this LLM plugin.
        """
        pass


    @abstractmethod
    def generate(self, prompt: str, **kwargs,) -> LLMResponse:
        """
        Generate a response for the given prompt.
        """
        pass