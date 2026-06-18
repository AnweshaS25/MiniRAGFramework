from src.loaders.pdf_loader import PDFLoader
from src.splitters.character_text_splitter import CharacterTextSplitter
from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings

#Load the PDF
loader = PDFLoader("data/BTechProject1_Final.pdf")
documents = loader.load()

#Split into chunks
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split(documents)

#Generate embeddings
embeddings = HuggingFaceEmbeddings()
embedded_chunks = embeddings.embed_documents(chunks)

#Assertions:
assert len(documents) > 0, "No documents were loaded."

assert len(chunks) > len(documents), (
    "Splitter did not create additional chunks."
)

assert len(embedded_chunks) == len(chunks), (
    "Some chunks were not embedded."
)

assert embedded_chunks[0].embedding is not None, (
    "Embedding was not added to the document."
)

assert isinstance(embedded_chunks[0].embedding, list), (
    "Embedding should be stored as a list."
)

assert len(
    embedded_chunks[0].embedding
) == 384


#Results
print(f"Original documents: {len(documents)}")
print(f"Chunks created: {len(chunks)}")
print(f"Embedded chunks: {len(embedded_chunks)}")

print("\nFirst Embedded Document:")
print(embedded_chunks[0])

print("\nFirst 5 embedding values:")
print(embedded_chunks[0].embedding[:5])

print("\nAll tests passed successfully!")