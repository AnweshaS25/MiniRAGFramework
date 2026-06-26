from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """
    Stores retrieval evaluation metrics.
    """

    precision_at_k: float
    recall_at_k: float
    hit_rate: float
    mean_reciprocal_rank: float