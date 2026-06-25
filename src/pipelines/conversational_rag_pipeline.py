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
        retriever: BaseRetriever,
        prompt_template: BasePromptTemplate,
        llm: BaseLLM,
        reranker: BaseReranker,
        memory: BaseMemory,
    ):

        super().__init__(
            retriever=retriever,
            prompt_template=prompt_template,
            llm=llm,
            reranker=reranker,
        )

        self.memory = memory

    
    def _build_prompt(self, question: str, context: str,) -> str:

        history = self.memory.get_context()

        print("\n================ HISTORY ================\n")
        print(history)
        print("\n=========================================\n")

        return self.prompt_template.format(
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