from src.query_rewriting.base_query_rewriter import BaseQueryRewriter
from src.memory.memory_manager import MemoryManager


class QueryRewriterManager:
    """
    Coordinates query rewriting before retrieval.
    """

    def __init__(self, rewriter: BaseQueryRewriter):

        if rewriter is None:
            raise ValueError("rewriter cannot be None.")

        self.rewriter = rewriter

    def rewrite(
        self,
        query: str,
        memory: MemoryManager,
    ) -> str:

        return self.rewriter.rewrite(
            query=query,
            memory=memory,
        )