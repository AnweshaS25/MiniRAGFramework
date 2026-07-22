import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.loaders.csv_loader import CSVLoader

print("===== Test Started =====")

loader = CSVLoader("data/sample.csv")

documents = loader.load()

print(f"Loaded {len(documents)} document(s)\n")

for doc in documents:
    print(doc.content)
    print(doc.metadata)