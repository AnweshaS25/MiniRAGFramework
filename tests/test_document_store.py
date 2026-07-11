from src.loaders.pdf_loader import PDFLoader
from src.document_store.in_memory_document_store import InMemoryDocumentStore


pdf_path = "data/BTechProject1_Final.pdf"

loader = PDFLoader(pdf_path)

documents = loader.load()

store = InMemoryDocumentStore()

store.add_documents(documents)

print(f"Loaded pages: {len(documents)}")
print(f"Stored pages: {len(store.get_documents())}")

print()

for document in store.get_documents()[:2]:
    print(document.metadata)