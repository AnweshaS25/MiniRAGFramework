from typing import List

from src.core.evaluation_sample import EvaluationSample
from src.core.evaluation_report import EvaluationReport
from src.core.evaluation_record import EvaluationRecord

from src.evaluation.rag_evaluator import RAGEvaluator
from src.pipelines.rag_pipeline import RAGPipeline


class EvaluationRunner:

    def __init__(self, pipeline: RAGPipeline, evaluator: RAGEvaluator,):
        self.pipeline = pipeline
        self.evaluator = evaluator


    def run(self, samples: List[EvaluationSample],) -> EvaluationReport:
        """
        Run evaluation on a dataset.
        """

        if not samples:
            raise ValueError("Evaluation dataset cannot be empty.")

        records: List[EvaluationRecord] = []  # Every time we will evaluate one question, we'll create an EvaluationRecord and store it here.

        for sample in samples:

            response = self.pipeline.run(
                query=sample.question,
            )

            metrics = self.evaluator.evaluate(
                generated_answer=response.text,
                reference_answer=sample.reference_answer,
            )

            record = EvaluationRecord(
                question=sample.question,
                reference_answer=sample.reference_answer,
                generated_answer=response.text,
                metrics=metrics,
            )

            records.append(record)  # Each record contains everything about one evaluated question.

        average_exact_match = (
            sum(
                record.metrics.exact_match
                for record in records
            )
            / len(records)
        )

        average_rouge_l = (
            sum(
                record.metrics.rouge_l
                for record in records
            )
            / len(records)
        )

        average_bert_score = (
            sum(
                record.metrics.bert_score
                for record in records
            )
            / len(records)
        )


        return EvaluationReport(
            exact_match=average_exact_match,
            rouge_l=average_rouge_l,
            bert_score=average_bert_score,
            records=records,
        )