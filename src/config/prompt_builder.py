from src.prompts.prompt_registry import PromptRegistry
from src.prompts.prompt_manager import PromptManager

from src.prompts.default_prompt_template import DefaultPromptTemplate
from src.prompts.summary_prompt_template import SummaryPromptTemplate
from src.prompts.concise_prompt_template import ConcisePromptTemplate
from src.prompts.citation_prompt_template import CitationPromptTemplate

from src.prompt_routing.rule_based_prompt_router import RuleBasedPromptRouter

from src.constants import PromptRouterTypes


class PromptBuilder:

    def __init__(self, config):
        self.config = config

    def build(
        self,
        llm_manager,
    ):
        prompt_registry = PromptRegistry()

        prompt_registry.register_prompt(
            DefaultPromptTemplate()
        )

        prompt_registry.register_prompt(
            SummaryPromptTemplate()
        )

        prompt_registry.register_prompt(
            ConcisePromptTemplate()
        )

        prompt_registry.register_prompt(
            CitationPromptTemplate()
        )

        if self.config.prompt_router_type == PromptRouterTypes.RULE_BASED:

            prompt_router = RuleBasedPromptRouter()

        else:
            raise ValueError(
                f"Unsupported prompt router: {self.config.prompt_router_type}"
            )

        prompt_manager = PromptManager(
            router=prompt_router,
            registry=prompt_registry,
        )

        return prompt_manager