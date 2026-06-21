from src.loaders.pdf_loader import PDFLoader
from src.splitters.recursive_text_splitter import RecursiveTextSplitter
from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.chroma_vector_store import ChromaVectorStore

from src.pipelines.indexing_pipeline import IndexingPipeline

def main():
    print("Inside main")

    loader = PDFLoader("data/BTechProject1_Final.pdf")

    splitter = RecursiveTextSplitter()

    embedding_model = HuggingFaceEmbeddings()

    vector_store = ChromaVectorStore(
        collection_name="test_indexing_pipeline",
        persist_directory="./test_chroma_db",
    )


    pipeline = IndexingPipeline(
        loader=loader,
        splitter=splitter,
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    print("Running indexing pipeline...\n")

    chunks = pipeline.run()

    assert len(chunks) > 0
    assert chunks[0].embedding is not None
    assert isinstance(chunks[0].embedding, list)

    print(f"Indexed {len(chunks)} chunks.\n")

    print("First Chunk")
    print("-" * 40)
    print(chunks[0].content[:300])
    print()

    print("Embedding Dimension")
    print("-" * 40)
    print(len(chunks[0].embedding))
    print()

    query_embedding = embedding_model.embed_query(
        "Are Cart and Wishlist used here?"
    )

    results = vector_store.similarity_search(
        query_embedding=query_embedding,
        k=2,
    )

    assert len(results) > 0

    assert results[0].content


    print(f"Retrieved {len(results)} documents from the vector store.\n")

    print("Top Retrieved Document")
    print("-" * 40)
    print(results[0].content)
    print()

    print("Metadata")
    print("-" * 40)
    print(results[0].metadata)

    print("IndexingPipeline test passed!")


if __name__ == "__main__":
    main()