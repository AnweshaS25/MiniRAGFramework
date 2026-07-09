from src.llm_routing.base_llm_router import BaseLLMRouter
from src.constants import LLMTypes

from src.core.llm_request import LLMRequest


class RuleBasedLLMRouter(BaseLLMRouter):
    """
    Simple rule-based LLM router.
    """

    SUMMARY_KEYWORDS = [
        "summarize",
        "summary",
        "overview",
    ]

    FAST_KEYWORDS = [
        "brief",
        "quick",
        "short",
    ]

    LOCAL_KEYWORDS = [
        "offline",
        "local",
        "private",
    ]

    def route(self, query: str) -> LLMRequest:

        if not query.strip():
            raise ValueError("query cannot be empty.")

        query = query.lower()

        # Long summarization → strongest model
        for keyword in self.SUMMARY_KEYWORDS:
            if keyword in query:
                return LLMRequest(
                    llm_type=LLMTypes.GROQ,
                )

        # User explicitly wants local inference
        for keyword in self.LOCAL_KEYWORDS:
            if keyword in query:
                return LLMRequest(
                    llm_type=LLMTypes.OLLAMA
                )

        # Short/simple question → Gemini Flash
        for keyword in self.FAST_KEYWORDS:
            if keyword in query:
                return LLMRequest(
                    llm_type=LLMTypes.GEMINI
                )

        # Default
        return LLMRequest(
            llm_type=LLMTypes.GROQ,
        )