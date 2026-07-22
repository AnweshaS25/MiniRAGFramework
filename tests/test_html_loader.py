import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.loaders.html_loader import HTMLLoader

print("===== Test Started =====")

loader = HTMLLoader("data/sample.html")

documents = loader.load()

print(f"Loaded {len(documents)} document(s)\n")

for doc in documents:
    print(doc.content)
    print(doc.metadata)