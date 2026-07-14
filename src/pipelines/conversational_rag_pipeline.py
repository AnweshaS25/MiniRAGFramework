from src.memory.base_memory import BaseMemory
from src.pipelines.rag_pipeline import RAGPipeline

from src.retrievers.base_retriever import BaseRetriever
from src.prompts.base_prompt_template import BasePromptTemplate
from src.llms.base_llm import BaseLLM
from src.rerankers.base_reranker import BaseReranker

from src.core.llm_response import LLMResponse

class ConversationalRAGPipeline(RAGPipeline):
    """
    RAG pipeline with conversation memory support.
    """

    def __init__(
        self,
        retriever,
        prompt_manager,
        document_store,
        llm_manager,
        reranker,
        context_manager,
        token_budget_strategy,
        security_guard,
        output_guard,
        tool_manager,
        memory,
    ):

        super().__init__(
            retriever=retriever,
            prompt_manager=prompt_manager,
            document_store=document_store,
            llm_manager=llm_manager,
            reranker=reranker,
            context_manager=context_manager,
            token_budget_strategy=token_budget_strategy,
            security_guard=security_guard,
            output_guard=output_guard,
            tool_manager=tool_manager,
        )

        self.memory = memory

    
    def _build_prompt(self, question: str, context: str,) -> str:

        history = self.memory.get_context()

        print("\n================ HISTORY ================\n")
        print(history)
        print("\n=========================================\n")

        prompt_template = self.prompt_manager.get_prompt_template(question)

        return prompt_template.format(
            question=question,
            context=context,
            history=history,
        )
    

    def _after_generation(self, query: str, response: LLMResponse,) -> None:

        self.memory.add_message(
            role="user",
            content=query,
        )

        self.memory.add_message(
            role="assistant",
            content=response.text,
        )