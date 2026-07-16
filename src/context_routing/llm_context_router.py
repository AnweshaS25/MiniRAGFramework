import json

from src.context_routing.base_context_router import BaseContextRouter
from src.core.context_request import ContextRequest

from src.llms.llm_manager import LLMManager


class LLMContextRouter(BaseContextRouter):
    """
    Uses an LLM to decide which context strategy should be used.
    """

    def __init__(self, llm_manager: LLMManager, prompt_template, registry):

        if llm_manager is None:
            raise ValueError(
                "llm_manager cannot be None."
            )

        self.llm_manager = llm_manager
        self.prompt_template = prompt_template
        self.registry = registry

    def route(self, query: str):

        prompt = self.prompt_template.build(
            query=query,
            registry=self.registry,
        )

        response = self.llm_manager.generate(
            query=query,
            prompt=prompt,
        )

        print("Context Router raw response:")
        print(response.text)

        cleaned = response.text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")
            cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            return None

        return ContextRequest(
            context_strategy=data["context_strategy"]
        )