from pathlib import Path

from src.core.retrieval_evaluation_sample import RetrievalEvaluationSample

import json

from pathlib import Path

from src.core.document_id import DocumentID
from src.core.retrieval_evaluation_sample import RetrievalEvaluationSample


class RetrievalDatasetLoader:
    """
    Loads retrieval benchmark datasets.
    """

    def load(
        self,
        dataset_path: str | Path,
    ) -> list[RetrievalEvaluationSample]:
        path = Path(dataset_path)

        with open(path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        samples = []

        for item in raw_data:
            relevant_ids = {
                (
                    doc["source"],
                    doc["page"],
                )
                for doc in item["relevant_ids"]
            }

            sample = RetrievalEvaluationSample(
                question=item["question"],
                relevant_ids=relevant_ids,
            )

            samples.append(sample)

        return samples