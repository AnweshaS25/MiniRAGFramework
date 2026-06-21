from src.loaders.pdf_loader import PDFLoader

from src.splitters.recursive_text_splitter import RecursiveTextSplitter

from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings

from src.vectorstores.chroma_vector_store import ChromaVectorStore

from src.retrievers.similarity_retriever import SimilarityRetriever

from src.prompts.default_prompt_template import DefaultPromptTemplate

from src.llms.groq_llm import GroqLLM

from src.pipelines.indexing_pipeline import IndexingPipeline
from src.pipelines.rag_pipeline import RAGPipeline


def main():

    print("=" * 50)
    print("MiniRAG PDF Assistant")
    print("=" * 50)
    print()

    pdf_path = input("Enter PDF path: ").strip()

    if not pdf_path:
        print("PDF path cannot be empty.")
        return
    
    print()
    print("Loading PDF... Please wait!")

    loader = PDFLoader(pdf_path)

    splitter = RecursiveTextSplitter()

    embedding_model = HuggingFaceEmbeddings()

    vector_store = ChromaVectorStore(
        collection_name="pdf_assistant",
        persist_directory="./pdf_assistant_db",
    )

    indexing_pipeline = IndexingPipeline(
        loader=loader,
        splitter=splitter,
        embedding_model=embedding_model,
        vector_store=vector_store,
    )


    print("Indexing document...\n")

    chunks = indexing_pipeline.run()

    print(f"Indexed {len(chunks)} chunks successfully!\n")

    retriever = SimilarityRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    prompt_template = DefaultPromptTemplate()

    llm = GroqLLM()

    rag_pipeline = RAGPipeline(
        retriever=retriever,
        prompt_template=prompt_template,
        llm=llm,
    )

    print("PDF Assistant is ready!")
    print("Type 'exit' to quit.\n")


    while True:

        question = input("You: ").strip()

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        try:

            response = rag_pipeline.run(
                query=question,
                k=3,
            )

            print()
            print("Assistant:")
            print("-" * 40)
            print(response.text)
            print()

        except Exception as e:
            print(f"\nError: {e}\n")



if __name__ == "__main__":
    main()