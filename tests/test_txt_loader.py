import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.loaders.txt_loader import TXTLoader

print("===== Test Started =====")

loader = TXTLoader("data/sample.txt")

documents = loader.load()

print(f"Loaded {len(documents)} document(s)\n")

for doc in documents:
    print(doc.content)
    print(doc.metadata)