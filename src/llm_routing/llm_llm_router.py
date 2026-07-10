import json
import re

from src.llm_routing.base_llm_router import BaseLLMRouter
from src.core.llm_request import LLMRequest


class LLMLLMRouter(BaseLLMRouter):
    """
    Uses an LLM to decide which LLM plugin should answer a query.
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

        print("LLM Router raw response:")
        print(response.text)

        match = re.search(r"\{.*\}", response.text, re.DOTALL)

        if not match:
            return None

        response_text = match.group(0)

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            return None

        return LLMRequest(
            llm_type=data["llm_type"],
            arguments={}
        )