from typing import List

from src.core.document_id import DocumentID
from src.evaluation.retrieval_evaluator import RetrievalEvaluator

from src.core.retrieval_evaluation_sample import RetrievalEvaluationSample


class RetrievalEvaluationRunner:
    """
    Runs retrieval evaluation on benchmark queries.
    """

    def __init__(
        self,
        retriever,
        evaluator: RetrievalEvaluator,
    ):
        self.retriever = retriever
        self.evaluator = evaluator

    def run(
        self,
        samples: list[RetrievalEvaluationSample],
        k: int = 5,
    ):
        results = []

        for sample in samples:

            retrieved_documents = self.retriever.retrieve(
                query=sample.question,
                k=k,
            )

            print("\n" + "=" * 70)
            print("QUESTION:")
            print(sample.question)

            print("\nRETRIEVED:")
            for doc in retrieved_documents:
                print(doc)

            print("\nEXPECTED:")
            print(sample.relevant_ids)

            print("\nQuestion:", sample.question)
            print("Retrieved IDs:")

            for doc_id in retrieved_documents:
                print(doc_id)

            print("Expected IDs:")
            print(sample.relevant_ids)
            print()

            # print("\n========== RETRIEVED DOCUMENTS ==========\n")

            # for doc in retrieved_documents:
            #     print(doc.metadata)

            # print("\n=========================================\n")

            # retrieved_ids = [
            #     (
            #         doc.metadata["source"],
            #         doc.metadata["page"],
            #     )
            #     for doc in retrieved_documents
            # ]

            metrics = self.evaluator.evaluate(
                # retrieved_ids=retrieved_ids,
                retrieved_ids=retrieved_documents,
                relevant_ids=sample.relevant_ids,
                k=k,
            )

            results.append(metrics)


        if not results:
            return {}

        return {
            "precision_at_k": sum(m.precision_at_k for m in results) / len(results),
            "recall_at_k": sum(m.recall_at_k for m in results) / len(results),
            "hit_rate": sum(m.hit_rate for m in results) / len(results),
            "mean_reciprocal_rank": (
                sum(m.mean_reciprocal_rank for m in results) / len(results)
            ),
            "records": results,
        }