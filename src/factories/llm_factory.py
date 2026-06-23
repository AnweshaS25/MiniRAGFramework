from src.llms.groq_llm import GroqLLM

from src.constants import LLMTypes

class LLMFactory:
    """
    Factory class for creating Large Language Models.
    """

    @staticmethod
    def create(llm_type: str, **kwargs,):

        if LLMTypes.GROQ:
            return GroqLLM()
        
        raise ValueError(
            f"Unsupported LLM: {llm_type}"
        )