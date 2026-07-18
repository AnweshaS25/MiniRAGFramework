from src.pipelines.conversational_rag_pipeline import (
    ConversationalRAGPipeline,
)


class PipelineBuilder:
    """
    Builds the conversational RAG pipeline.
    """

    def __init__(self, config):

        self.config = config

    def build(
        self,
        components,
    ):
        return ConversationalRAGPipeline(

            retriever=components.core["retriever"],
            prompt_manager=components.prompt_manager,
            document_store=components.document_store,
            llm_manager=components.llm_manager,
            reranker=components.reranker,
            context_manager=components.context_manager,
            token_budget_strategy=components.token_budget_strategy,
            security_guard=components.security_guard,
            output_guard=components.output_guard,
            tool_manager=components.tool_manager,
            memory=components.memory,
            query_rewriter=components.query_rewriter,
            memory_retriever=components.memory_retriever,

            timer=components.timer,
        )