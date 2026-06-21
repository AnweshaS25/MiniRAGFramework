from src.core.document import Document

from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.in_memory_vector_store import InMemoryVectorStore


def main():

    print("Inside main")

    embedding_model = HuggingFaceEmbeddings()

    vector_store = InMemoryVectorStore()

    document = Document(
        content="MiniRAG is a Retrieval-Augmented Generation framework.",
        metadata={"source": "test"},
    )

    embedding_model.embed_documents([document])

    vector_store.add_documents([document])

    query_embedding = embedding_model.embed_query(
        "What is MiniRAG?"
    )

    results = vector_store.similarity_search(
        query_embedding=query_embedding,
        k=1,
    )

    assert len(results) == 1

    print("Document added successfully!")

    vector_store.clear()

    results = vector_store.similarity_search(
        query_embedding=query_embedding,
        k=1,
    )

    assert len(results) == 0

    print("Vector store cleared successfully!")

    print("InMemoryVectorStore clear() test passed!")


if __name__ == "__main__":
    main()