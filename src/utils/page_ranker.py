from collections import defaultdict
from typing import List

from src.core.document import Document

from collections import Counter


class PageRanker:
    """
    Groups retrieved chunks by page while preserving
    their retrieval order.
    """

    @staticmethod
    def rank_pages(retrieved_chunks: List[Document],) -> List[tuple[str, int]]:

        counts = Counter()

        for chunk in retrieved_chunks:

            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")

            counts[(source, page)] += 1

        ranked_pages = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            page
            for page, _ in ranked_pages
        ]