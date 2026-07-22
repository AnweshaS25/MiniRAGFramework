from dataclasses import dataclass

from src.core.document_id import DocumentID


@dataclass
class RetrievalEvaluationSample:
    """
    Represents one retrieval evaluation example.
    """

    question: str

    # relevant_ids: set[DocumentID]
    relevant_ids: set[int]