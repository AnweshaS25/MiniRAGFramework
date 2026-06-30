from src.strategies.default_context_strategy import DefaultContextStrategy


class ContextStrategyFactory:
    """
    Factory class for creating context strategies.
    """

    @staticmethod
    def create():
        return DefaultContextStrategy()