from src.strategies.base_context_strategy import BaseContextStrategy
from typing import List
from src.core.document import Document


class DefaultContextStrategy(BaseContextStrategy):
    """
    Default heuristic for deciding retrieval size
    based on the LLM context window.
    """

    name = "default"

    description = (
        "Uses semantic retrieval from the vector store to retrieve the most "
        "relevant chunks before answering."
    )

    def get_top_k(self, context_window: int,) -> int:

        if context_window <= 8_000:
            return 3

        if context_window <= 32_000:
            return 8

        if context_window <= 128_000:
            return 20

        return 40
    
    def build_context(self, documents: List[Document],) -> str:

        context_parts = []

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown",
            )

            page = document.metadata.get(
                "page",
                "Unknown",
            )

            context_parts.append(
                f"Source: {source}\n"
                f"Page: {page}\n\n"
                f"{document.content}"
            )

        return "\n\n----------------------------------------\n\n".join(
            context_parts
        )
    

    def requires_retrieval(self):
        return True