from src.strategies.base_context_strategy import BaseContextStrategy

from collections import defaultdict
from typing import List
from src.core.document import Document


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
    

    def build_context(self, documents: List[Document],) -> str:

        grouped = defaultdict(dict)

        for document in documents:

            source = document.metadata.get("source", "Unknown")
            page = document.metadata.get("page", 0)

            grouped[source][page] = document.content

        context_parts = []

        for source, pages in grouped.items():

            context_parts.append(
                f"========== Document: {source} ==========\n"
            )

            for page in sorted(pages.keys()):

                context_parts.append(
                    f"\n----- Page {page} -----\n\n"
                    f"{pages[page]}"
                )

        return "\n".join(context_parts)
    

    def requires_retrieval(self):
        return False