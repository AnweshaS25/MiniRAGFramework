from src.core.rag_evaluation_result import RAGEvaluationResult

from src.evaluation.base_evaluator import BaseEvaluator
from src.evaluation.metrics.generation_metrics import (exact_match, rouge_l, bert_score_metric,)


class RAGEvaluator(BaseEvaluator):
    """
    Evaluates generated answers.
    """

    def evaluate(self, generated_answer: str, reference_answer: str,) -> RAGEvaluationResult:

        return RAGEvaluationResult(
            exact_match=exact_match(
                generated_answer,
                reference_answer,
            ),

            rouge_l=rouge_l(
                generated_answer,
                reference_answer,
            ),

            bert_score=bert_score_metric(
                generated_answer,
                reference_answer,
            ),
        )
    