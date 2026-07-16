from src.query_rewriting.base_query_rewriter import BaseQueryRewriter
from src.memory.memory_manager import MemoryManager


class RuleBasedQueryRewriter(BaseQueryRewriter):
    """
    Very simple query rewriter.

    If the query appears incomplete (contains pronouns like 'it',
    'they', 'that', etc.), prepend the recent conversation history.
    """

    PRONOUNS = [
        "it",
        "they",
        "them",
        "that",
        "those",
        "this",
        "these",
        "its",
    ]

    def rewrite(
        self,
        query: str,
        memory: MemoryManager,
    ) -> str:

        lowered = query.lower()

        # If the query already looks self-contained,
        # leave it unchanged.
        if not any(word in lowered.split() for word in self.PRONOUNS):
            return query

        history = memory.get_context()

        if not history.strip():
            return query

        return (
            f"Conversation History:\n"
            f"{history}\n\n"
            f"Current Question:\n"
            f"{query}"
        )