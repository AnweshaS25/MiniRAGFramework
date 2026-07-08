from src.tool_routing.base_tool_router import BaseToolRouter

import json
from src.core.tool_request import ToolRequest


class LLMToolRouter(BaseToolRouter):
    """
    Tool router that uses an LLM to decide which tool to invoke.
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
        
        return ToolRequest(
            tool_name=data["tool"],
            arguments=data.get("arguments", {}),
        )