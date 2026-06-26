from dataclasses import dataclass


@dataclass
class EvaluationSample:
    """
    Represents one evaluation example.
    """

    question: str

    reference_answer: str