from src.llm_routing.base_llm_router import BaseLLMRouter
from src.factories.llm_factory import LLMFactory


class LLMManager:
    """
    Coordinates LLM routing and LLM creation.
    """

    def __init__(self, router: BaseLLMRouter):

        if router is None:
            raise ValueError("router cannot be None.")

        self.router = router

    def get_llm(self, query: str, **kwargs):

        llm_request = self.router.route(query)

        if llm_request is None:
            raise ValueError(
                "LLM router failed to select an LLM."
            )

        llm_kwargs = dict(kwargs)

        llm_kwargs.update(llm_request.arguments)

        return LLMFactory.create(
            llm_request.llm_type,
            **llm_kwargs,
        )