from dataclasses import dataclass


@dataclass
class RAGEvaluationResult:
    """
    Stores RAG evaluation metrics.
    """

    exact_match: float
    rouge_l: float
    bert_score: float