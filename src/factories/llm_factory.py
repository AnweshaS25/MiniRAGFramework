from src.llms.groq_llm import GroqLLM
from src.llms.ollama_llm import OllamaLLM

from src.constants import LLMTypes

class LLMFactory:
    """
    Factory class for creating Large Language Models.
    """

    @staticmethod
    def create(llm_type: str, **kwargs,):
        
        if llm_type == LLMTypes.GROQ:
            return GroqLLM()
        
        elif llm_type == LLMTypes.OLLAMA:
            return OllamaLLM(
                model=kwargs.get(
                    "model",
                    "llama3.2",
                ),
                host=kwargs.get(
                    "host",
                    "http://localhost:11434",
                ),
                temperature=kwargs.get(
                    "temperature",
                    0.7,
                ),
            )
        
        raise ValueError(
            f"Unsupported LLM: {llm_type}"
        )