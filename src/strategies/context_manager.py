from src.context_routing.base_context_router import BaseContextRouter
from src.strategies.context_registry import ContextRegistry


class ContextManager:
    """
    Coordinates context routing and strategy selection.
    """

    def __init__(self, router: BaseContextRouter, registry: ContextRegistry,):

        self.router = router
        self.registry = registry

    def get_strategy(self, query: str,):

        context_request = self.router.route(query)

        if context_request is None:
            raise ValueError(
                "Context router failed to select a strategy."
            )

        strategy_name = self.router.route(query)

        print(f"Context Router selected: {strategy_name}")

        strategy = self.registry.get_strategy(context_request.context_strategy)

        if strategy is None:
            raise ValueError(
                f"Unknown context strategy '{context_request.context_strategy}'."
            )

        return strategy