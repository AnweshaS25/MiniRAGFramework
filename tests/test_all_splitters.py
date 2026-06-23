from src.core.document import Document

from src.splitters.character_text_splitter import CharacterTextSplitter
from src.splitters.recursive_text_splitter import RecursiveTextSplitter
from src.splitters.token_text_splitter import TokenTextSplitter


TEXT = """
Retrieval-Augmented Generation (RAG) is a technique that combines
information retrieval with large language models.

Instead of relying only on the knowledge stored inside the language model,
RAG retrieves relevant documents from an external knowledge base.

The retrieved context is then inserted into the prompt before sending it
to the language model.

This improves factual accuracy and reduces hallucinations.
""" * 5


def print_chunks(name, chunks, token_splitter=None):

    print("\n")
    print("=" * 80)
    print(name)
    print("=" * 80)

    print(f"\nTotal Chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks, start=1):

        print("-" * 60)
        print(f"Chunk {i}")

        print(chunk.content)

        print()

        print(f"Characters: {len(chunk.content)}")

        if token_splitter is not None:

            token_count = len(
                token_splitter.encoding.encode(
                    chunk.content
                )
            )

            print(f"Tokens: {token_count}")

        print("-" * 60)


def main():

    document = Document(content=TEXT)

    character_splitter = CharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=50,
    )

    recursive_splitter = RecursiveTextSplitter(
        chunk_size=250,
        chunk_overlap=50,
    )

    token_splitter = TokenTextSplitter(
        chunk_size=60,
        chunk_overlap=10,
    )

    character_chunks = character_splitter.split([document])

    recursive_chunks = recursive_splitter.split([document])

    token_chunks = token_splitter.split([document])

    print_chunks(
        "Character Splitter",
        character_chunks,
    )

    print_chunks(
        "Recursive Splitter",
        recursive_chunks,
    )

    print_chunks(
        "Token Splitter",
        token_chunks,
        token_splitter,
    )


if __name__ == "__main__":
    main()