from src.prompt_routing.base_prompt_router import BasePromptRouter
from src.core.prompt_request import PromptRequest
from src.constants import PromptTemplateTypes


class RuleBasedPromptRouter(BasePromptRouter):
    """
    Simple rule-based prompt router.
    """

    SUMMARY_KEYWORDS = [
        "summarize",
        "summary",
        "overview",
        "gist",
        "brief summary",
    ]

    CONCISE_KEYWORDS = [
        "brief",
        "short",
        "concise",
        "quick",
        "one line",
        "two lines",
    ]

    CITATION_KEYWORDS = [
        "cite",
        "citation",
        "source",
        "where did",
        "according to",
        "which page",
    ]

    def route(self, query: str) -> PromptRequest:

        query = query.lower()

        for keyword in self.SUMMARY_KEYWORDS:
            if keyword in query:
                return PromptRequest(
                    prompt_type=PromptTemplateTypes.SUMMARY
                )

        for keyword in self.CONCISE_KEYWORDS:
            if keyword in query:
                return PromptRequest(
                    prompt_type=PromptTemplateTypes.CONCISE
                )

        for keyword in self.CITATION_KEYWORDS:
            if keyword in query:
                return PromptRequest(
                    prompt_type=PromptTemplateTypes.CITATION
                )

        return PromptRequest(
            prompt_type=PromptTemplateTypes.DEFAULT
        )