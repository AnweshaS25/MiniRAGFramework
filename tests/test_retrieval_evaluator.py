from src.evaluation.retrieval_evaluator import RetrievalEvaluator


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
    }

    evaluator = RetrievalEvaluator()

    result = evaluator.evaluate(
        retrieved_ids=retrieved,
        relevant_ids=relevant,
        k=5,
    )

    print("=" * 50)
    print("Retrieval Evaluation")
    print("=" * 50)

    print(f"Precision@5 : {result.precision_at_k:.3f}")
    print(f"Recall@5    : {result.recall_at_k:.3f}")
    print(f"Hit Rate    : {result.hit_rate:.3f}")
    print(f"MRR         : {result.mean_reciprocal_rank:.3f}")


if __name__ == "__main__":
    main()