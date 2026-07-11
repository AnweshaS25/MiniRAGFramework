from src.strategies.base_context_strategy import BaseContextStrategy


class HybridContextStrategy(BaseContextStrategy):
    """
    Hybrid strategy that retrieves more context than
    traditional RAG while still using retrieval.

    Intended for large-context models where we want
    more information than Top-K retrieval but don't
    necessarily load the entire corpus.
    """

    def get_top_k(self, context_window: int) -> int:

        if context_window >= 500000:
            return 1000

        elif context_window >= 100000:
            return 250

        else:
            return 50