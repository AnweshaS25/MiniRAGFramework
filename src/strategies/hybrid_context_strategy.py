from src.strategies.base_context_strategy import BaseContextStrategy

from collections import defaultdict
from typing import List
from src.core.document import Document


class HybridContextStrategy(BaseContextStrategy):
    """
    Hybrid strategy that retrieves more context than
    traditional RAG while still using retrieval.

    Intended for large-context models where we want
    more information than Top-K retrieval but don't
    necessarily load the entire corpus.
    """

    name = "hybrid"

    description = (
        "Combines semantic retrieval with broader contextual information to "
        "produce more comprehensive answers."
    )

    def get_top_k(self, context_window: int) -> int:

        if context_window >= 500000:
            return 1000

        elif context_window >= 100000:
            return 250

        else:
            return 50
        
    
    def build_context(
            self, 
            retrieved_chunks: List[Document], 
            original_documents: List[Document] | None = None,
    ) -> str:

        grouped = defaultdict(list)

        for document in retrieved_chunks:

            source = document.metadata.get("source", "Unknown")
            page = document.metadata.get("page", "Unknown")

            key = (source, page)

            grouped[key].append(document.content)

        retrieved_parts = []

        for (source, page), chunks in grouped.items():

            merged_text = "\n\n".join(chunks)

            retrieved_parts.append(
                f"===== {source} | Page {page} =====\n\n"
                f"{merged_text}"
            )

        retrieved_context = "\n\n----------------------------------------\n\n".join(
            retrieved_parts
        )

        if not original_documents:
            return retrieved_context
        
        original_parts = []

        for document in original_documents:

            source = document.metadata.get("source", "Unknown")
            page = document.metadata.get("page", "Unknown")

            original_parts.append(
                f"===== {source} | Page {page} =====\n\n"
                f"{document.content}"
            )

        original_context = "\n\n----------------------------------------\n\n".join(
            original_parts
        )

        return f"""
==============================
Retrieved Relevant Chunks
==============================

{retrieved_context}

==============================
Original Document Context
==============================

{original_context}
"""
    

    def requires_retrieval(self):
        return True