from src.core.document import Document
from src.splitters.sentence_splitter import SentenceSplitter

document = Document(
    content="""
RAG is a retrieval technique.
Embeddings convert text into vectors.
ChromaDB stores vectors.
Cross encoders rerank results.
LLMs generate answers.
""",
    metadata={
        "source": "test",
    },
)

splitter = SentenceSplitter( chunk_size=2,)

chunks = splitter.split([document],)

print("="*60)

for index, chunk in enumerate(
    chunks,
    start=1,
):
    print(f"chunk {index}")

    print(chunk.content)

    print("-" * 60)