from src.core.document import Document

from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.in_memory_vector_store import InMemoryVectorStore
from src.retrievers.similarity_retriever import SimilarityRetriever

def main():

    # Create embedding model
    embedding_model = HuggingFaceEmbeddings()

    # Create vector store
    vector_store = InMemoryVectorStore()

    # Create sample documents
    documents = [
        Document(
            content="Cats are small domestic animals.",
            metadata={"source": "doc1"},
        ),
        Document(
            content="Cats love sleeping in the sun.",
            metadata={"source": "doc2"},
        ),
        Document(
            content="Dogs are loyal companions.",
            metadata={"source": "doc3"},
        ),
    ]

    # Generate embeddings
    embedding_model.embed_documents(documents)

    # Store documents
    vector_store.add_documents(documents)

    # Create retriever
    retriever = SimilarityRetriever(embedding_model=embedding_model,vector_store=vector_store,)

    # Retrieve
    results = retriever.retrieve(query="Cats",k=2,)

    print(f"\nRetrieved {len(results)} documents\n")

    for i, document in enumerate(results, start=1):
        print(f"Result {i}")
        print("-" * 40)
        print(document.content)
        print(document.metadata)
        print()

    # Basic assertions
    assert len(results) == 2

    for document in results:
        assert "cat" in document.content.lower()

    print("SimilarityRetriever test passed!")



if __name__ == "__main__":
        main()