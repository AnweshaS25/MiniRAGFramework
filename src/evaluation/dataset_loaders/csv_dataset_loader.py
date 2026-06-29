import csv
from typing import List

from src.core.evaluation_sample import EvaluationSample

from src.evaluation.dataset_loaders.base_dataset_loader import BaseDatasetLoader


class CSVDatasetLoader(BaseDatasetLoader):
    """
    Loads evaluation samples from a CSV file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path


    def load(self) -> List[EvaluationSample]:
        """
        Load evaluation samples from CSV.
        """

        samples = []

        with open(
            self.file_path,
            mode="r",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                sample = EvaluationSample(
                    question=row["question"],
                    reference_answer=row["reference_answer"],
                )

                samples.append(sample)

        return samples