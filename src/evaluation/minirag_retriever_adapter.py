from typing import List

from src.core.document_id import DocumentID


class MiniRAGRetrieverAdapter:
    """
    Makes the MiniRAG retriever compatible with
    RetrievalEvaluationRunner.
    """

    def __init__(self, retriever):
        self.retriever = retriever

    def retrieve(
        self,
        query: str,
        k: int,
    ) -> List[DocumentID]:

        documents = self.retriever.retrieve(
            query=query,
            k=k,
        )

        seen = set()
        document_ids = []

        for doc in documents:

            doc_id = (
                doc.metadata["source"],
                doc.metadata["page"],
            )

            if doc_id not in seen:
                seen.add(doc_id)
                document_ids.append(doc_id)

        return document_ids