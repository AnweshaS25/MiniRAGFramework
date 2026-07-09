import json

from src.prompt_routing.base_prompt_router import BasePromptRouter
from src.core.prompt_request import PromptRequest


class LLMPromptRouter(BasePromptRouter):
    """
    Prompt router that uses an LLM to decide which prompt template to use.
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

        response_text = response.text

        try:
            data = json.loads(response_text)

        except json.JSONDecodeError:
            return None

        if data is None:
            return None

        print("Prompt Router selected:", data["prompt_type"])

        return PromptRequest(
            prompt_type=data["prompt_type"],
        )