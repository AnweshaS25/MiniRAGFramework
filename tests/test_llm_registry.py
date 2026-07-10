from src.llms.llm_registry import LLMRegistry

from src.llms.groq_llm import GroqLLM
from src.llms.gemini_llm import GeminiLLM
from src.llms.ollama_llm import OllamaLLM

from src.constants import LLMTypes

registry = LLMRegistry()

registry.register_llm(
    LLMTypes.GROQ,
    GroqLLM(),
)

registry.register_llm(
    LLMTypes.GEMINI,
    GeminiLLM(),
)

registry.register_llm(
    LLMTypes.OLLAMA,
    OllamaLLM(),
)

for metadata in registry.list_metadata():
    print(metadata)