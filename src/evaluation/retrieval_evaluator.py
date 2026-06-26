from src.evaluation.base_evaluator import BaseEvaluator
from typing import Set
from src.core.evaluation_result import EvaluationResult
from src.evaluation.metrics.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
    hit_rate,
    mean_reciprocal_rank,
)


class RetrievalEvaluator(BaseEvaluator):
    """
    Evaluates retrieval performance.
    """

    def evaluate(self, retrieved_ids: list[str], relevant_ids: Set[str], k: int,) -> EvaluationResult:

        if k <= 0:
            raise ValueError("k must be greater than 0.")

        return EvaluationResult(
            precision_at_k=precision_at_k(
                retrieved_ids,
                relevant_ids,
                k,
            ),
            recall_at_k=recall_at_k(
                retrieved_ids,
                relevant_ids,
                k,
            ),
            hit_rate=hit_rate(
                retrieved_ids,
                relevant_ids,
                k,
            ),
            mean_reciprocal_rank=mean_reciprocal_rank(
                retrieved_ids,
                relevant_ids,
                k,
            ),
        )