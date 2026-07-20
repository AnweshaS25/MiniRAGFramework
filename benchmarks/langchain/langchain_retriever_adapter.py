from typing import List

from src.core.document_id import DocumentID


class LangChainRetrieverAdapter:
    """
    Makes a LangChain retriever compatible with the
    RetrievalEvaluationRunner.
    """

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def retrieve(
        self,
        query: str,
        k: int,
    ) -> List[DocumentID]:
        
        documents = self.pipeline.retrieve(
            query=query,
            k=k,
        )

        seen = set()
        document_ids = []

        for doc in documents:

            doc_id = (
                doc.metadata["source"],
                doc.metadata["page"] + 1,
            )

            if doc_id not in seen:
                seen.add(doc_id)
                document_ids.append(doc_id)

        return document_ids