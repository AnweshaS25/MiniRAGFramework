from src.evaluation.metrics.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
    hit_rate,
    mean_reciprocal_rank,
)

def main():

    retrieved = [
        "doc1",
        "doc2",
        "doc3",
        "doc4",
        "doc5",
    ]

    relevant = {
        "doc1",
        "doc3",
        "doc5",
        "doc8",
        "doc9",
    }

    precision = precision_at_k(
        retrieved,
        relevant,
        k=5,
    )

    recall = recall_at_k(
        retrieved,
        relevant,
        k=5,
    )

    hit = hit_rate(
        retrieved,
        relevant,
        k=5,
    )

    mrr = mean_reciprocal_rank(
        retrieved,
        relevant,
        k=5,
    )

    print(f"Precision@5 : {precision:.2f}")
    print(f"Recall@5    : {recall:.2f}")
    print(f"Hit Rate@5   : {hit:.2f}")
    print(f"MRR@5        : {mrr:.3f}")


if __name__ == "__main__":
    main()