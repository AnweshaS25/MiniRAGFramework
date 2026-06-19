from src.loaders.pdf_loader import PDFLoader
from src.splitters.character_text_splitter import CharacterTextSplitter
from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.in_memory_vector_store import InMemoryVectorStore

#Load the PDF
loader = PDFLoader("data/BTechProject1_Final.pdf")
documents = loader.load()

#Split into chunks
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split(documents)

#Generate embeddings
embedder = HuggingFaceEmbeddings()
embedded_chunks = embedder.embed_documents(chunks)

#Creating vector store
vector_store = InMemoryVectorStore()
vector_store.add_documents(embedded_chunks)

query = "What is the purpose of the project?"

#Embedding the query
query_embedding = embedder.embed_query(query)

results = vector_store.similarity_search(
    query_embedding = query_embedding,
    k=3
)

print("Retrieved Documents:")

for i, document in enumerate(results, start=1):
    print(f"\nResult {i}")
    print(document.metadata)
    print(document.content[:300])

# Assertions
assert len(results) == 3
assert all(result.embedding is not None for result in results)
assert all(len(result.embedding) == 384 for result in results)
assert all(result.content for result in results)

print("\n✅ InMemoryVectorStore test passed successfully!")