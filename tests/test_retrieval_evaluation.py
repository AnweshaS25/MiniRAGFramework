import shutil
from pathlib import Path

from src.config.framework_builder import FrameworkBuilder
from src.config.framework_config import FrameworkConfig

from src.constants import LoaderTypes
from src.constants import SplitterTypes
from src.constants import EmbeddingTypes
from src.constants import VectorStoreTypes
from src.constants import RetrieverTypes
from src.constants import LLMTypes
from src.constants import PromptRouterTypes
from src.constants import ToolRouterTypes
from src.constants import ContextRouterTypes
from src.constants import QueryRewriterTypes
from src.constants import SecurityTypes
from src.constants import RerankerTypes

from src.evaluation.dataset_loaders.retrieval_dataset_loader import RetrievalDatasetLoader
from src.evaluation.retrieval_evaluation_runner import RetrievalEvaluationRunner
from src.evaluation.retrieval_evaluator import RetrievalEvaluator

from src.evaluation.minirag_retriever_adapter import (
    MiniRAGRetrieverAdapter,
)


if __name__ == "__main__":

    pdf_path = "data/BTechProject1_Final.pdf"

    config = FrameworkConfig(
        loader_type=LoaderTypes.PDF,
        splitter_type=SplitterTypes.RECURSIVE,
        embedding_type=EmbeddingTypes.HUGGINGFACE,
        vector_store_type=VectorStoreTypes.CHROMA,
        retriever_type=RetrieverTypes.SIMILARITY,

        llm_types=[
            LLMTypes.GROQ,
            LLMTypes.GEMINI,
            LLMTypes.OLLAMA,
        ],

        conversation_window_size=2,
        summarize_after=6,

        prompt_router_type=PromptRouterTypes.RULE_BASED,
        tool_router_type=ToolRouterTypes.LLM,
        context_router_type=ContextRouterTypes.RULE_BASED,
        query_rewriter_type=QueryRewriterTypes.LLM,

        security_type=SecurityTypes.LLM,
        reranker_type=RerankerTypes.NONE,

        persist_directory="./test_chroma_db",
    )

    test_db = Path("./test_chroma_db")

    if test_db.exists():
        shutil.rmtree(test_db)

    builder = FrameworkBuilder(config)

    framework = builder.build(pdf_path)

    framework.indexing_pipeline.run(
        metadata={
            "permission": "VIEW_HR_DOCUMENTS",
        }
    )

    loader = RetrievalDatasetLoader()

    samples = loader.load(
        "tests/data/retrieval_dataset.json",
    )

    adapter = MiniRAGRetrieverAdapter(
        framework.core["retriever"],
    )

    runner = RetrievalEvaluationRunner(
        retriever=adapter,
        evaluator=RetrievalEvaluator(),
    )

    report = runner.run(
        samples=samples,
        k=5,
    )

    print("\n========== RETRIEVAL EVALUATION REPORT ==========\n")

    print(report)

    print("\n========== PER-QUESTION RESULTS ==========\n")

    for sample, record in zip(samples, report["records"]):
        print("-" * 60)
        print("Question:")
        print(sample.question)
        print()
        print("Relevant IDs:")
        print(sample.relevant_ids)
        print()
        print("Metrics:")
        print(record)