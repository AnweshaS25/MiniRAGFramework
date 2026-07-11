from src.strategies.base_context_strategy import BaseContextStrategy


class ContextRegistry:
    """
    Registry for all available context strategies.
    """

    def __init__(self):
        self._strategies = {}

    def register_strategy(self, name: str, strategy: BaseContextStrategy,):
        self._strategies[name] = strategy

    def get_strategy(self, name: str,):
        return self._strategies.get(name)

    def list_strategies(self):
        return self._strategies