from src.evaluation.dataset_loaders.csv_dataset_loader import CSVDatasetLoader


loader = CSVDatasetLoader(
    file_path="tests/data/evaluation_dataset.csv",
)

samples = loader.load()

print("=" * 50)

for sample in samples:
    print(f"Question : {sample.question}")
    print(f"Reference: {sample.reference_answer}")
    print("-" * 50)