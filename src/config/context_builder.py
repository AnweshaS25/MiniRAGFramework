from src.strategies.context_registry import ContextRegistry
from src.strategies.context_manager import ContextManager

from src.strategies.default_context_strategy import DefaultContextStrategy
from src.strategies.hybrid_context_strategy import HybridContextStrategy
from src.strategies.lcm_context_strategy import LCMContextStrategy

from src.context_routing.rule_based_context_router import RuleBasedContextRouter
from src.context_routing.llm_context_router import LLMContextRouter

from src.prompts.context_router_prompt import ContextRouterPrompt

from src.constants import ContextRouterTypes


class ContextBuilder:
    """
    Builds the context subsystem.
    """

    def __init__(self, config):

        self.config = config

    def build(
        self,
        llm_manager,
    ):
        context_registry = ContextRegistry()

        context_registry.register_strategy(
            "default",
            DefaultContextStrategy(),
        )

        context_registry.register_strategy(
            "hybrid",
            HybridContextStrategy(),
        )

        context_registry.register_strategy(
            "lcm",
            LCMContextStrategy(),
        )

        if self.config.context_router_type == ContextRouterTypes.RULE_BASED:

            context_router = RuleBasedContextRouter()

        elif self.config.context_router_type == ContextRouterTypes.LLM:

            context_router = LLMContextRouter(
                llm_manager=llm_manager,
                prompt_template=ContextRouterPrompt(),
                registry=context_registry,
            )

        else:

            raise ValueError(
                f"Unsupported context router: {self.config.context_router_type}"
            )

        context_manager = ContextManager(
            router=context_router,
            registry=context_registry,
        )   

        return context_manager