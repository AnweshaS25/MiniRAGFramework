from src.config.framework_config import FrameworkConfig

from src.llms.llm_registry import LLMRegistry
from src.llms.llm_manager import LLMManager

from src.factories.llm_factory import LLMFactory
from src.factories.llm_manager_factory import LLMManagerFactory

from src.llm_routing.rule_based_llm_router import RuleBasedLLMRouter
from src.llm_strategies.default_fallback_strategy import DefaultFallbackStrategy

from src.constants import LLMTypes



class LLMBuilder:
    """
    Builds all LLM-related components.
    """

    def __init__(self, config: FrameworkConfig):

        if config is None:
            raise ValueError("config cannot be None.")

        self.config = config



    def build(self) -> LLMManager:
        """
        Build the LLM registry and manager.
        """

        registry = LLMRegistry()

        for llm_type in self.config.llm_types:

            llm = LLMFactory.create(llm_type)

            registry.register_llm(
                llm_type,
                llm,
            )

        router = RuleBasedLLMRouter()

        fallback_strategy = DefaultFallbackStrategy()

        llm_manager = LLMManagerFactory.create(
            router=router,
            registry=registry,
            fallback_strategy=fallback_strategy,
        )   

        return llm_manager