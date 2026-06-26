from src.core.evaluation_sample import EvaluationSample

from src.evaluation.rag_evaluator import RAGEvaluator
from src.evaluation.evaluation_runner import EvaluationRunner

from src.factories.splitter_factory import SplitterFactory
from src.factories.loader_factory import LoaderFactory
from src.factories.embedding_factory import EmbeddingFactory
from src.factories.vector_store_factory import VectorStoreFactory
from src.factories.retriever_factory import RetrieverFactory
from src.factories.llm_factory import LLMFactory

from src.prompts.default_prompt_template import DefaultPromptTemplate

from src.pipelines.indexing_pipeline import IndexingPipeline

from src.constants import (
    SplitterTypes,
    LoaderTypes,
    EmbeddingTypes,
    VectorStoreTypes,
    RetrieverTypes,
    LLMTypes,
)

from src.pipelines.rag_pipeline import RAGPipeline

from src.rerankers.cross_encoder_reranker import CrossEncoderReranker

print("=" * 60)
print("Creating components")
print("=" * 60)

loader = LoaderFactory.create(
    LoaderTypes.PDF,
    file_path="data/evaluation_data.pdf",
)

splitter = SplitterFactory.create(
    SplitterTypes.RECURSIVE,
)

embedding_model = EmbeddingFactory.create(
    EmbeddingTypes.HUGGINGFACE,
)

vector_store = VectorStoreFactory.create(
    VectorStoreTypes.CHROMA,
    collection_name="evaluation_collection",
    persist_directory="./evaluation_chroma",
)

vector_store.clear()

indexing_pipeline = IndexingPipeline(
    loader=loader,
    splitter=splitter,
    embedding_model=embedding_model,
    vector_store=vector_store,
)

indexing_pipeline.run()


retriever = RetrieverFactory.create(
    RetrieverTypes.SIMILARITY,
    embedding_model=embedding_model,
    vector_store=vector_store,
)

prompt_template = DefaultPromptTemplate()

llm = LLMFactory.create(
    LLMTypes.GROQ,
)

reranker = CrossEncoderReranker()

pipeline = RAGPipeline(
    retriever=retriever,
    prompt_template=prompt_template,
    llm=llm,
    reranker=reranker,
)

evaluator = RAGEvaluator()

runner = EvaluationRunner(
    pipeline=pipeline,
    evaluator=evaluator,
)

samples = [
    EvaluationSample(
        question="What is RAG?",
        reference_answer="RAG stands for Retrieval-Augmented Generation.",
    ),

    EvaluationSample(
        question="What is ChromaDB?",
        reference_answer="ChromaDB is a vector database.",
    ),

    EvaluationSample(
        question="What are embeddings?",
        reference_answer="Embeddings are numerical vector representations of data.",
    ),
]

report = runner.run(samples)

print()
print("=" * 60)
print("Evaluation Report")
print("=" * 60)

print(f"Average Exact Match : {report.exact_match:.3f}")
print(f"Average ROUGE-L     : {report.rouge_l:.3f}")
print(f"Average BERTScore   : {report.bert_score:.3f}")

print()
print("=" * 60)
print("Per Question Results")
print("=" * 60)

for record in report.records:

    print()

    print(f"Question : {record.question}")

    print(f"Generated : {record.generated_answer}")

    print(f"Reference : {record.reference_answer}")

    print(
        f"Exact Match = {record.metrics.exact_match:.3f}"
    )

    print(
        f"ROUGE-L     = {record.metrics.rouge_l:.3f}"
    )

    print(
        f"BERTScore   = {record.metrics.bert_score:.3f}"
    )

    print("-" * 60)