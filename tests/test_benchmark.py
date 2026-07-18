from src.evaluation.benchmark_runner import BenchmarkRunner

from src.config.framework_config import FrameworkConfig
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

from src.config.framework_builder import FrameworkBuilder


# def run_benchmark(
#     framework,
# ):

#     runner = BenchmarkRunner(
#         pipeline=framework.pipeline,
#     )

#     queries = [
#         "What is RAG?",
#         "Explain GraphRAG.",
#         "What is LangChain?",
#     ]

#     summary = runner.run(
#         queries=queries,
#     )

#     print(summary)


pdf_path = 'data/BTechProject1_Final.pdf'


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
)
    

builder = FrameworkBuilder(config)

framework = builder.build(pdf_path)

from src.auth.user import User
from src.factories.role_factory import RoleFactory
from src.constants import RoleTypes

    # document_store = framework.document_store
    # indexing_pipeline = framework.indexing_pipeline
    # tool_manager = framework.tool_manager
    # prompt_manager = framework.prompt_manager
    # memory = framework.memory
    # context_manager = framework.context_manager
    # query_rewriter = framework.query_rewriter
    # memory_retriever = framework.memory_retriever
    # reranker = framework.reranker
    # security_guard = framework.security_guard
    # output_guard = framework.output_guard
    # token_budget_strategy = framework.token_budget_strategy

rag_pipeline = framework.pipeline

benchmark_user = User(
    username="benchmark_user",
    roles=[
        RoleFactory.create(RoleTypes.ADMIN),
    ],
)

runner = BenchmarkRunner(
    pipeline=rag_pipeline,
)

queries = [
    "What is this project about?",
    "What are the functional dependencies?",
    "Is there data flow diagrams present here?",
]

summary = runner.run(
    queries=queries,
    user=benchmark_user,
)

print("\n========== BENCHMARK SUMMARY ==========\n")
print(summary)