from src.strategies.base_context_strategy import BaseContextStrategy


class LCMContextStrategy(BaseContextStrategy):
    """
    Context strategy for Large Context Models (LCMs).

    Instead of retrieving only a few chunks,
    this strategy attempts to use the entire document
    whenever the model context window allows.
    """

    def get_top_k(self, context_window: int) -> int:
        """
        For LCMs, retrieve a very large number of chunks.
        The pipeline will later trim them according
        to the token budget.
        """

        return 100000