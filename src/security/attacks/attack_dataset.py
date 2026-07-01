import json
from pathlib import Path
from src.core.document import Document


class AttackDataset:
    """
    Loads known attack prompts.
    """

    DEFAULT_DATASET_PATH = (
        Path(__file__).parent / "prompt_injection_dataset.json"
    )

    def __init__(self, dataset_path: str | Path = DEFAULT_DATASET_PATH):
        self.dataset_path = Path(dataset_path)
        self.attack_prompts = self._load()

    def _load(self) -> list[str]:

        with open(self.dataset_path, "r") as f:
            return json.load(f)
        
    def get_documents(self) -> list[Document]:
        """
        Convert attack prompts into Document objects.
        """

        documents = []

        for prompt in self.attack_prompts:
            documents.append(
                Document(
                    content=prompt,
                    metadata={
                        "source": "attack_dataset",
                    },
                )
            )

        return documents