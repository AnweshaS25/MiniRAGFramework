from src.query_rewriting.query_rewriter_manager import QueryRewriterManager
from src.query_rewriting.llm_query_rewriter import LLMQueryRewriter

from src.memory_retrieval.memory_retriever_manager import MemoryRetrieverManager
from src.memory_retrieval.keyword_memory_retriever import KeywordMemoryRetriever

from src.constants import QueryRewriterTypes


class QueryBuilder:
    """
    Builds the query preprocessing subsystem.
    """

    def __init__(self, config):

        self.config = config

    def build(
        self,
        llm_manager,
    ):
        if self.config.query_rewriter_type == QueryRewriterTypes.LLM:

            query_rewriter = QueryRewriterManager(
                rewriter=LLMQueryRewriter(
                    llm_manager=llm_manager,
                ),
            )

        else:

            raise ValueError(
                f"Unsupported query rewriter: {self.config.query_rewriter_type}"
            )

        memory_retriever = MemoryRetrieverManager(
            retriever=KeywordMemoryRetriever(),
        )

        return {
            "query_rewriter": query_rewriter,
            "memory_retriever": memory_retriever,
        }