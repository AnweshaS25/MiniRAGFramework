from src.loaders.pdf_loader import PDFLoader
from src.splitters.character_text_splitter import CharacterTextSplitter

loader = PDFLoader("data/BTechProject1_Final.pdf")
documents = loader.load()

splitter = CharacterTextSplitter(500, 100)
chunks = splitter.split(documents)

print(f"Original documents: {len(documents)}")
print(f"Chunks created: {len(chunks)}")

for chunk in chunks[:5]:
    print(chunk)

print(chunks[0].metadata)
print(chunks[1].metadata)

for i, chunk in enumerate(chunks[:10]):
    print(f"Chunk {i + 1}")
    print(chunk.metadata)
    print(f"Length: {len(chunk.content)}")
    print("-" * 40)
