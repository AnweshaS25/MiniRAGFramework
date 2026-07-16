from src.tool_routing.base_tool_router import BaseToolRouter

from src.llms.llm_manager import LLMManager

import json
from src.core.tool_request import ToolRequest


class LLMToolRouter(BaseToolRouter):
    """
    Tool router that uses an LLM to decide which tool to invoke.
    """

    def __init__(self, llm_manager:LLMManager, prompt_template, registry):

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

        response_text = response.text

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            return None
        
        if data is None:
            return None
        

        print("Parsed JSON:", data)
        print("Tool field :", data.get("tool"))
        print("Arguments  :", data.get("arguments"))
        
        return ToolRequest(
            tool_name=data["tool"],
            arguments=data.get("arguments", {}),
        )