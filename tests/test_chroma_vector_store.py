from src.vectorstores.chroma_vector_store import ChromaVectorStore
from src.core.document import Document

import os    #To check whether the database already exists
import shutil  #To delete the test database before starting

def main():
    # Remove old test database (if it exists)
    if os.path.exists("./test_chroma_db"):
        shutil.rmtree("./test_chroma_db")

    # Create a fresh vector store
    store = ChromaVectorStore(
        collection_name="test_collection",
        persist_directory="./test_chroma_db",
    )

    # Create sample documents
    documents = [
        Document(
            content="Cats are small domestic animals.",
            metadata={"source": "doc1"},
            embedding=[0.10, 0.20, 0.30],
        ),
        Document(
            content="Cats love sleeping in the sun.",
            metadata={"source": "doc2"},
            embedding=[0.11, 0.19, 0.31],
        ),
        Document(
            content="Artificial intelligence is transforming healthcare.",
            metadata={"source": "doc3"},
            embedding=[0.90, 0.80, 0.70],
        ),
    ]


    # Add documents
    store.add_documents(documents)
    print("Documents added successfully!\n")

    # Perform similarity search
    query_embedding = [0.10, 0.20, 0.30]

    results = store.similarity_search(
        query_embedding=query_embedding,
        k=2,
    )

    # Print retrieved results
    print(f"Retrieved {len(results)} documents\n")

    for i, document in enumerate(results, start=1):
        print(f"Result {i}")
        print("-" * 40)
        print(document.content)
        print()
        print(document.metadata)
        print()

    # Assertions
    assert isinstance(results, list)
    assert len(results) <= 2

    for document in results:
        assert isinstance(document, Document)
        assert document.content
        assert isinstance(document.metadata, dict)


    print("ChromaVectorStore test passed!")

if __name__ == "__main__":
    main()