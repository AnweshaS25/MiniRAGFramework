import json
from typing import List

from src.core.evaluation_sample import EvaluationSample

from src.evaluation.dataset_loaders.base_dataset_loader import BaseDatasetLoader


class JSONDatasetLoader(BaseDatasetLoader):
    """
    Loads evaluation samples from a JSON file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path


    def load(self) -> List[EvaluationSample]:
        """
        Load evaluation samples from JSON.
        """

        with open(
            self.file_path,
            mode="r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        samples = []

        for item in data:

            sample = EvaluationSample(
                question=item["question"],
                reference_answer=item["reference_answer"],
            )

            samples.append(sample)

        return samples