from src.loaders.pdf_loader import PDFLoader
from src.splitters.recursive_text_splitter import RecursiveTextSplitter

# Load PDF
loader = PDFLoader("data/BTechProject1_Final.pdf")
documents = loader.load()

# Create splitter
splitter = RecursiveTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

# Split documents
chunks = splitter.split(documents)

print(f"Number of chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:5], start=1):
    print(f"\nChunk {i}")
    print("-" * 40)
    print(chunk.metadata)
    print("\nLength of this chunk: ")
    print(len(chunk.content))
    print(chunk.content)

assert len(chunks) > 0
assert all(chunk.content for chunk in chunks)
assert all(chunk.metadata for chunk in chunks)

assert all(
    isinstance(chunk.content, str)
    for chunk in chunks
)

assert all(
    len(chunk.content) <= splitter.chunk_size
    for chunk in chunks
), "Some chunks exceed the configured chunk_size."

print("\n RecursiveTextSplitter basic test passed!")