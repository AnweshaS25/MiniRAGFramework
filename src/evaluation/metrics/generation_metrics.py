from typing import Set
from rouge_score import rouge_scorer
from bert_score import score

def exact_match(generated_answer: str, reference_answer: str,) -> float:
    """
    Compute Exact Match score.
    """

    if not generated_answer.strip():
        return 0.0

    if not reference_answer.strip():
        return 0.0

    generated = generated_answer.strip().lower()

    reference = reference_answer.strip().lower()

    return float(
        generated == reference
    )


def rouge_l(generated_answer: str, reference_answer: str,) -> float:
    """
    Compute ROUGE-L F1 score.
    """

    if not generated_answer.strip():
        return 0.0

    if not reference_answer.strip():
        return 0.0

    scorer = rouge_scorer.RougeScorer(
        ["rougeL"],
        use_stemmer=True,
    )

    scores = scorer.score(
        reference_answer,
        generated_answer,
    )

    return scores["rougeL"].fmeasure



def bert_score_metric(
    generated_answer: str,
    reference_answer: str,
    model_name: str = "microsoft/deberta-xlarge-mnli",
) -> float:
    """
    Compute BERTScore F1.
    """

    if not generated_answer.strip():
        return 0.0

    if not reference_answer.strip():
        return 0.0

    _, _, f1 = score(
        [generated_answer],
        [reference_answer],
        model_type=model_name,
        lang="en",
        verbose=False,
    )

    return float(f1.item())