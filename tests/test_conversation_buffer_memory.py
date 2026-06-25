from src.factories.memory_factory import MemoryFactory
from src.constants import MemoryTypes


def main():

    memory = MemoryFactory.create(
        MemoryTypes.CONVERSATION_BUFFER
    )

    memory.add_message(
        role="user",
        content="What is RAG?"
    )

    memory.add_message(
        role="assistant",
        content="Retrieval-Augmented Generation is..."
    )

    memory.add_message(
        role="user",
        content="Explain it simply."
    )

    print(memory.get_context())

    print("\nClearing memory...\n")

    memory.clear()

    print(repr(memory.get_context()))


if __name__ == "__main__":
    main()