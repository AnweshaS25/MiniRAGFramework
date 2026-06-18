from src.loaders.pdf_loader import PDFLoader

loader = PDFLoader("data/BTechProject1_Final.pdf")

documents = loader.load()

print(f"Number of documents: {len(documents)}")

for doc in documents:
    print(doc)