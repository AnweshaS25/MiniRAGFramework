from dataclasses import dataclass

from src.core.rag_evaluation_result import RAGEvaluationResult


@dataclass
class EvaluationRecord:   # one EvaluationRecord = one evaluated question.
    """
    Stores the evaluation result for one question.
    """

    question: str
    reference_answer: str
    generated_answer: str
    metrics: RAGEvaluationResult 