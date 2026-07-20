from benchmarks.langchain.langchain_pipeline import LangChainPipeline

from benchmarks.langchain.langchain_retriever_adapter import (
    LangChainRetrieverAdapter,
)

from src.evaluation.dataset_loaders.retrieval_dataset_loader import (
    RetrievalDatasetLoader,
)

from src.evaluation.retrieval_evaluation_runner import (
    RetrievalEvaluationRunner,
)

from src.evaluation.retrieval_evaluator import (
    RetrievalEvaluator,
)

from src.evaluation.dataset_loaders.json_dataset_loader import JSONDatasetLoader
from benchmarks.langchain.langchain_generation_adapter import (
    LangChainGenerationAdapter,
)
from src.evaluation.evaluation_runner import EvaluationRunner

from src.evaluation.rag_evaluator import RAGEvaluator

if __name__ == "__main__":

    pipeline = LangChainPipeline(
        "data/BTechProject1_Final.pdf"
    )

    


    # Load
    documents = pipeline.load_documents()

    print(f"Loaded {len(documents)} pages")

    # Split
    chunks = pipeline.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Index
    pipeline.index_documents(chunks)
    print("Indexed documents successfully.")

    adapter = LangChainRetrieverAdapter(pipeline)


    # Retrieve
    # retrieved_docs = pipeline.retrieve(
    #     "What is this project about?"
    # )

    # print("\n========== RETRIEVED DOCUMENTS ==========\n")

    # for i, doc in enumerate(retrieved_docs, start=1):
    #     print(f"\n---------- Document {i} ----------")

    #     print(doc.metadata)

    #     print()

    #     print(doc.page_content[:150])

    #     print("----------------------------------")

    # print("\n=========================================\n")

    loader = RetrievalDatasetLoader()

    samples = loader.load(
        "tests/data/retrieval_dataset.json",
    )

    runner = RetrievalEvaluationRunner(
        retriever=adapter,
        evaluator=RetrievalEvaluator(),
    )

    report = runner.run(
        samples=samples,
        k=5,
    )

    print("\n========== LANGCHAIN RETRIEVAL REPORT ==========\n")

    print(report)


    # =========================
    # GENERATION BENCHMARK
    # =========================

    generation_adapter = LangChainGenerationAdapter(pipeline)

    generation_loader = JSONDatasetLoader(
        "tests/data/generation_dataset.json"
    )

    generation_samples = generation_loader.load()

    generation_runner = EvaluationRunner(
        pipeline=generation_adapter,
        evaluator=RAGEvaluator(),
    )

    generation_report = generation_runner.run(
        samples=generation_samples,
        user=None,
    )

    print("\n========== LANGCHAIN GENERATION REPORT ==========\n")

    print(generation_report)