from src.llm_routing.base_llm_router import BaseLLMRouter
from src.llms.llm_registry import LLMRegistry
from src.llm_strategies.base_fallback_strategy import BaseFallbackStrategy


class LLMManager:
    """
    Coordinates LLM routing and LLM creation.
    """

    def __init__(self, router: BaseLLMRouter, registry: LLMRegistry, fallback_strategy: BaseFallbackStrategy,):

        if router is None:
            raise ValueError("router cannot be None.")
        
        if registry is None:
            raise ValueError("registry cannot be None.")
        
        if fallback_strategy is None:
            raise ValueError("fallback_strategy cannot be None.")

        self.router = router
        self.registry = registry
        self.fallback_strategy = fallback_strategy

    def get_llm(self, query: str, **kwargs):

        llm_request = self.router.route(query)

        if llm_request is None:
            raise ValueError(
                "LLM router failed to select an LLM."
            )

        llm = self.registry.get_llm(
            llm_request.llm_type
        )

        if llm is None:
            raise ValueError(
                f"LLM '{llm_request.llm_type}' is not registered."
            )

        return llm
    

    def get_llm_chain(self, query: str):
        """
        Returns the ordered LLM chain using the configured fallback strategy.
        """

        preferred_llm = self.get_llm(query)

        return self.fallback_strategy.order(
            preferred_llm=preferred_llm,
            available_llms=self.registry.get_all_llms(),
        )