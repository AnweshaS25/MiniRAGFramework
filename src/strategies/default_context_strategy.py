from src.strategies.base_context_strategy import BaseContextStrategy


class DefaultContextStrategy(BaseContextStrategy):
    """
    Default heuristic for deciding retrieval size
    based on the LLM context window.
    """

    def get_top_k(self, context_window: int,) -> int:

        if context_window <= 8_000:
            return 3

        if context_window <= 32_000:
            return 8

        if context_window <= 128_000:
            return 20

        return 40