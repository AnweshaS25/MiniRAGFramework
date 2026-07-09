from src.llm_routing.base_llm_router import BaseLLMRouter
from src.llms.llm_registry import LLMRegistry


class LLMManager:
    """
    Coordinates LLM routing and LLM creation.
    """

    def __init__(self, router: BaseLLMRouter, registry: LLMRegistry,):

        if router is None:
            raise ValueError("router cannot be None.")
        
        if registry is None:
            raise ValueError("registry cannot be None.")

        self.router = router
        self.registry = registry

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