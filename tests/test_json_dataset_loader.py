from src.evaluation.dataset_loaders.json_dataset_loader import JSONDatasetLoader


loader = JSONDatasetLoader(
    file_path="tests/data/evaluation_dataset.json",
)

samples = loader.load()

print("=" * 50)

for sample in samples:

    print(f"Question : {sample.question}")
    print(f"Reference: {sample.reference_answer}")

    print("-" * 50)