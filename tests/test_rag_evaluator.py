from src.evaluation.rag_evaluator import RAGEvaluator


def main():

    evaluator = RAGEvaluator()

    result = evaluator.evaluate(
        generated_answer="Paris is the capital of France.",
        reference_answer="The capital of France is Paris.",
    )

    print("=" * 50)
    print("RAG Evaluation")
    print("=" * 50)

    print(f"Exact Match : {result.exact_match}")
    print(f"ROUGE-L     : {result.rouge_l:.3f}")
    print(f"BERTScore   : {result.bert_score:.3f}")


if __name__ == "__main__":
    main()