import shutil
from pathlib import Path

from src.config.framework_builder import FrameworkBuilder
from src.config.framework_config import FrameworkConfig

from src.auth.user import User
from src.factories.role_factory import RoleFactory
from src.constants import RoleTypes

from src.constants import (
    LoaderTypes,
    SplitterTypes,
    EmbeddingTypes,
    VectorStoreTypes,
    RetrieverTypes,
    LLMTypes,
    PromptRouterTypes,
    ToolRouterTypes,
    ContextRouterTypes,
    QueryRewriterTypes,
    SecurityTypes,
    RerankerTypes,
)

from src.evaluation.dataset_loaders.json_dataset_loader import JSONDatasetLoader
from src.evaluation.evaluation_runner import EvaluationRunner
from src.evaluation.rag_evaluator import RAGEvaluator



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

    test_user = User(
        username="benchmark_user",
        roles=[
            RoleFactory.create(RoleTypes.ADMIN),
        ],
    )

    framework.indexing_pipeline.run(
        metadata={
            "permission": "VIEW_HR_DOCUMENTS",
        }
    )

    loader = JSONDatasetLoader(
        "tests/data/generation_dataset.json",
    )

    samples = loader.load()

    runner = EvaluationRunner(
        pipeline=framework.pipeline,
        evaluator=RAGEvaluator(),
    )

    report = runner.run(
        samples=samples,
        user=test_user,
    )

    print("\n========== GENERATION EVALUATION REPORT ==========\n")

    print(report)