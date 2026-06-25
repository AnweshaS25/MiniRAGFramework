from src.factories.reranker_factory import RerankerFactory
from src.constants import RerankerTypes
from src.core.document import Document
from src.rerankers.cross_encoder_reranker import CrossEncoderReranker



def main():

    reranker = RerankerFactory.create(RerankerTypes.CROSS_ENCODER,)

    query = "What is Retrieval-Augmented Generation?"

    documents = [
        Document(
            content="RAG combines retrieval and generation to answer questions.",
            metadata={},
        ),
        Document(
            content="Cats are small domesticated mammals.",
            metadata={},
        ),
        Document(
            content="Retrieval-Augmented Generation retrieves relevant documents before generating an answer.",
            metadata={},
        ),
    ]

    reranked = reranker.rerank(
        query=query,
        documents=documents,
        top_k=3,
    )

    print("\nReranked Documents:\n")

    for i, doc in enumerate(reranked, start=1):
        print(f"{i}. {doc.content}")


if __name__ == "__main__":
    main()