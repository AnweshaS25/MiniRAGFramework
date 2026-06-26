from dataclasses import dataclass
from typing import List

from src.core.evaluation_record import EvaluationRecord


@dataclass
class EvaluationReport:
    """
    Overall evaluation report.
    """

    exact_match: float
    rouge_l: float
    bert_score: float
    records: List[EvaluationRecord]   #the report now stores all evaluated questions.