from src.core.document import Document

from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings

from src.vectorstores.in_memory_vector_store import InMemoryVectorStore

from src.retrievers.similarity_retriever import SimilarityRetriever
from src.retrievers.mmr_retriever import MMRRetriever


def main():

    print("=" * 80)
    print("Creating embedding model")
    print("=" * 80)

    embedding_model = HuggingFaceEmbeddings()

    print("\nCreating documents...\n")

    documents = [

        Document(
            content="RAG combines retrieval with language models."
        ),

        Document(
            content="Retrieval-Augmented Generation combines retrieval with language models."
        ),

        Document(
            content="RAG retrieves documents before generation."
        ),

        Document(
            content="Embeddings convert text into vectors."
        ),

        Document(
            content="Vector databases store embeddings."
        ),
    ]

    print("Embedding documents...")

    embedding_model.embed_documents(documents)

    print("Creating vector store...")

    vector_store = InMemoryVectorStore()

    vector_store.add_documents(documents)

    query = "Explain Retrieval-Augmented Generation"

    print("\n")
    print("=" * 80)
    print("Similarity Retriever")
    print("=" * 80)

    similarity_retriever = SimilarityRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    similarity_results = similarity_retriever.retrieve(
        query=query,
        k=3,
    )

    for index, document in enumerate(similarity_results, start=1):
        print(f"\nResult {index}")
        print(document.content)

    print("\n")
    print("=" * 80)
    print("MMR Retriever")
    print("=" * 80)

    mmr_retriever = MMRRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        lambda_param=0.5,
        fetch_k=5,
    )

    mmr_results = mmr_retriever.retrieve(
        query=query,
        k=3,
    )

    for index, document in enumerate(mmr_results, start=1):
        print(f"\nResult {index}")
        print(document.content)


if __name__ == "__main__":
    print("Inside main")
    main()