import json

from src.context_routing.base_context_router import BaseContextRouter
from src.core.context_request import ContextRequest


class LLMContextRouter(BaseContextRouter):
    """
    Uses an LLM to decide which context strategy should be used.
    """

    def __init__(self, llm, prompt_template, registry):
        self.llm = llm
        self.prompt_template = prompt_template
        self.registry = registry

    def route(self, query: str):

        prompt = self.prompt_template.build(
            query=query,
            registry=self.registry,
        )

        response = self.llm.generate(prompt)

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