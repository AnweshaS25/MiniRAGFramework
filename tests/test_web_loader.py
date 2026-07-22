import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.loaders.web_loader import WebLoader

print("===== Test Started =====")

loader = WebLoader("https://example.com")

documents = loader.load()

print(f"Loaded {len(documents)} document(s)\n")

for doc in documents:
    print(doc.content[:500])   # Print only the first 500 characters
    print("\nMetadata:", doc.metadata)