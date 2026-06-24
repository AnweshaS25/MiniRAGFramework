from src.factories.vector_store_factory import VectorStoreFactory
from src.constants import VectorStoreTypes


def main():

    print("=" * 60)
    print("Testing InMemoryVectorStore")
    print("=" * 60)

    memory_store = VectorStoreFactory.create(
        VectorStoreTypes.IN_MEMORY
    )

    print(type(memory_store))

    print()

    print("=" * 60)
    print("Testing ChromaVectorStore")
    print("=" * 60)

    chroma_store = VectorStoreFactory.create(
        VectorStoreTypes.CHROMA,
        collection_name="test_collection",
        persist_directory="./test_chroma_db",
    )

    print(type(chroma_store))


if __name__ == "__main__":
    main()