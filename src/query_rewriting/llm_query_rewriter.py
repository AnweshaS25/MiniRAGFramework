from src.query_rewriting.base_query_rewriter import BaseQueryRewriter
from src.memory.memory_manager import MemoryManager
from src.llms.llm_manager import LLMManager


class LLMQueryRewriter(BaseQueryRewriter):
    """
    Uses an LLM to rewrite follow-up questions into
    standalone queries suitable for retrieval.
    """

    def __init__(self, llm_manager: LLMManager):

        if llm_manager is None:
            raise ValueError("llm_manager cannot be None.")

        self.llm_manager = llm_manager

    def rewrite(
        self,
        query: str,
        memory: MemoryManager,
    ) -> str:

        history = memory.get_context()

        if not history.strip():
            return query

        prompt = f"""
        You are a query rewriting assistant for a Retrieval-Augmented Generation (RAG) system.

        Your job is to rewrite follow-up questions into standalone questions.

        Conversation History:
        ---------------------
        {history}

        Current Question:
        -----------------
        {query}

        Instructions:
        - Rewrite the current question so that it is completely self-contained.
        - Replace pronouns such as "it", "they", "that", "those", etc. with the correct entities from the conversation.
        - Preserve the user's original intent.
        - Do NOT answer the question.
        - Do NOT explain your reasoning.
        - Return ONLY the rewritten question.

        Rewritten Question:
        """

        response = self.llm_manager.generate(
            query=query,
            prompt=prompt,
        )

        rewritten_query = response.text.strip()

        print("\n=========== LLM QUERY REWRITER ===========")
        print("Original :", query)
        print("Rewritten:", rewritten_query)
        print("==========================================\n")

        return rewritten_query