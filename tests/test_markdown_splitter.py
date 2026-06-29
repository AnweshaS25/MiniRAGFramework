from src.core.document import Document
from src.splitters.markdown_splitter import MarkdownSplitter


document = Document(
    content="""
# Introduction

RAG introduction.

# Embeddings

Embeddings explanation.

## Sentence Transformers

Sentence transformer details.

# ChromaDB

Vector database.
""",
    metadata={
        "source": "test.md",
    },
)


splitter = MarkdownSplitter()

chunks = splitter.split(
    [document],
)

print("=" * 60)
print("Markdown Splitter Test")
print("=" * 60)

for index, chunk in enumerate(
    chunks,
    start=1,
):

    print()

    print(f"Chunk {index}")

    print("-" * 60)

    print(chunk.content)

    print("-" * 60)