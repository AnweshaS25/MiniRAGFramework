from src.prompt_routing.rule_based_prompt_router import RuleBasedPromptRouter
from src.prompt_routing.llm_prompt_router import LLMPromptRouter

from src.constants import PromptRouterTypes


class PromptRouterFactory:
    """
    Factory for creating prompt routers.
    """

    @staticmethod
    def create(
        prompt_router_type: str,
        **kwargs,
    ):

        if prompt_router_type == PromptRouterTypes.RULE_BASED:
            return RuleBasedPromptRouter()

        if prompt_router_type == PromptRouterTypes.LLM:

            llm = kwargs.get("llm")
            prompt_template = kwargs.get("prompt_template")

            if llm is None:
                raise ValueError("llm is required.")

            if prompt_template is None:
                raise ValueError(
                    "prompt_template is required."
                )

            return LLMPromptRouter(
                llm=llm,
                prompt_template=prompt_template,
            )

        raise ValueError(
            f"Unsupported prompt router: {prompt_router_type}"
        )