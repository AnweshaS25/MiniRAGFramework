from src.core.document import Document

from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.chroma_vector_store import ChromaVectorStore


def main():

    print("Inside main")

    embedding_model = HuggingFaceEmbeddings()

    vector_store = ChromaVectorStore(
        collection_name="test_clear_collection",
        persist_directory="./test_chroma_db",
    )

    # Start with an empty collection
    vector_store.clear()

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

    print("Collection cleared successfully!")

    print("clear() test passed!")


if __name__ == "__main__":
    main()