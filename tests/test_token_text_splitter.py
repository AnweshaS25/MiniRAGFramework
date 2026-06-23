from src.core.document import Document
from src.splitters.token_text_splitter import TokenTextSplitter


def main():

    print("Inside main")

    splitter = TokenTextSplitter(
        chunk_size=20,
        chunk_overlap=5,
    )

    document = Document(
        content=(
            "This is a simple sentence. " * 30
        ),
        metadata={
            "source": "test.pdf",
            "page": 1,
        },
    )

    chunks = splitter.split([document])

    print(f"\nNumber of chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks, start=1):

        print("=" * 60)
        print(f"Chunk {i}")
        print("=" * 60)

        print(chunk.content)

        print("\nToken Count:",
            len(splitter.encoding.encode(chunk.content)))

        print()


    assert len(chunks) > 1

    for chunk in chunks:

        assert isinstance(chunk, Document)

        assert chunk.content != ""

        assert chunk.metadata == document.metadata

    print("TokenTextSplitter test passed!")


if __name__ == "__main__":
    main()











# from src.core.document import Document
# from src.splitters.token_text_splitter import TokenTextSplitter

# def test_invalid_chunk_size():

#     try:
#         TokenTextSplitter(chunk_size=0)
#         assert False

#     except ValueError:
#         assert True


# def test_invalid_chunk_overlap():

#     try:
#         TokenTextSplitter(
#             chunk_size=100,
#             chunk_overlap=100,
#         )
#         assert False

#     except ValueError:
#         assert True


# def test_split():

#     splitter = TokenTextSplitter(
#         chunk_size=20,
#         chunk_overlap=5,
#     )

#     document = Document(
#         content=(
#             "This is a simple sentence. "
#             * 30
#         )
#     )

#     chunks = splitter.split([document])

#     assert len(chunks) > 1

#     for chunk in chunks:

#         assert isinstance(chunk, Document)

#         assert chunk.content != ""


# def test_metadata_preserved():

#     splitter = TokenTextSplitter(
#         chunk_size=20,
#         chunk_overlap=5,
#     )

#     document = Document(
#         content="Hello world " * 30,
#         metadata={
#             "source": "test.pdf",
#             "page": 1,
#         },
#     )

#     chunks = splitter.split([document])

#     for chunk in chunks:
#         assert chunk.metadata == document.metadata