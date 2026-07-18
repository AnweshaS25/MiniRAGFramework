from src.memory.base_memory import BaseMemory
from src.pipelines.rag_pipeline import RAGPipeline
from src.memory.memory_manager import MemoryManager

from src.retrievers.base_retriever import BaseRetriever
from src.prompts.base_prompt_template import BasePromptTemplate
from src.llms.base_llm import BaseLLM
from src.rerankers.base_reranker import BaseReranker

from src.core.llm_response import LLMResponse

from src.memory_retrieval.memory_retriever_manager import MemoryRetrieverManager

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
        memory: MemoryManager,
        query_rewriter,
        memory_retriever: MemoryRetrieverManager,
        timer=None,
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
        self.query_rewriter = query_rewriter
        self.memory_retriever = memory_retriever
        self.timer = timer

    

    def _start_timer(
        self,
        stage: str,
    ):

        if self.timer is not None:
            self.timer.start(stage)



    def _stop_timer(
        self,
        stage: str,
    ):

        if self.timer is not None:
            self.timer.stop(stage)



    def _build_prompt(self, question: str, context: str,) -> str:

        print(">>> USING Conversational _build_prompt")

        # history = self.memory.get_context()

        history = self.memory_retriever.retrieve(
            query=question,
            memory=self.memory,
        )

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


    def run(
        self,
        query: str,
        user,
    ):
        """
        Rewrite conversational queries before running RAG.
        """

        self._start_timer("total")

        self._start_timer("query_rewriting")

        rewritten_query = self.query_rewriter.rewrite(
            query=query,
            memory=self.memory,
        )

        self._stop_timer("query_rewriting")

        print("\n=========== QUERY REWRITER ===========")
        print("Original :", query)
        print("Rewritten:", rewritten_query)
        print("======================================\n")

        response = super().run(
            query=rewritten_query,
            user=user,
        )

        self._stop_timer("total")

        return response