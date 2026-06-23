from src.embeddings.bge_embeddings import BGEEmbeddings


def main():

    print("Inside main")

    model = BGEEmbeddings()

    texts = [
        "Retrieval-Augmented Generation improves LLM responses.",
        "MiniRAG Framework is modular and extensible.",
    ]

    print("\nEmbedding Documents...\n")

    document_embeddings = model.embed_documents(texts)

    print(f"Number of document embeddings: {len(document_embeddings)}")

    print(
        f"Embedding dimension: {len(document_embeddings[0])}"
    )

    print("\nFirst 10 values of first embedding:\n")

    print(document_embeddings[0][:10])

    print("\nEmbedding Query...\n")

    query = "What is Retrieval-Augmented Generation?"

    query_embedding = model.embed_query(query)

    print(
        f"Query embedding dimension: {len(query_embedding)}"
    )

    print("\nFirst 10 values of query embedding:\n")

    print(query_embedding[:10])


if __name__ == "__main__":
    main()