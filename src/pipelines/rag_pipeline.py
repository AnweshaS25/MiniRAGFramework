from typing import List

from src.core.document import Document
from src.core.llm_response import LLMResponse

from src.pipelines.base_pipeline import BasePipeline

from src.retrievers.base_retriever import BaseRetriever
from src.prompts.base_prompt_template import BasePromptTemplate
from src.llms.base_llm import BaseLLM
from src.rerankers.base_reranker import BaseReranker

from src.strategies.base_context_strategy import BaseContextStrategy
from src.strategies.base_token_budget_strategy import BaseTokenBudgetStrategy


class RAGPipeline(BasePipeline):
    """
    Pipeline responsible for retrieving relevant documents,
    constructing the prompt, and generating the final answer.
    """

    def __init__(self, retriever: BaseRetriever, prompt_template: BasePromptTemplate,llm: BaseLLM, reranker: BaseReranker, context_strategy: BaseContextStrategy, token_budget_strategy: BaseTokenBudgetStrategy,):

        if retriever is None:
            raise ValueError("retriever cannot be None.")

        if prompt_template is None:
            raise ValueError("prompt_template cannot be None.")

        if llm is None:
            raise ValueError("llm cannot be None.")

        if reranker is None:
            raise ValueError("reranker cannot be None.")
        
        if context_strategy is None:
            raise ValueError("context_strategy cannot be None.")
        
        if token_budget_strategy is None:
            raise ValueError("token_budget_strategy cannot be None.")

        self.retriever = retriever
        self.prompt_template = prompt_template
        self.llm = llm
        self.reranker = reranker
        self.context_strategy = context_strategy
        self.token_budget_strategy = token_budget_strategy

    def _build_context(self, documents: List[Document],) -> str:
        context_parts = []

        for document in documents:
            source = document.metadata.get("source", "Unknown")
            page = document.metadata.get("page", "Unknown")

            context_parts.append(
                f"Source: {source}\n"
                f"Page: {page}\n\n"
                f"{document.content}"
            )

        return "\n\n----------------------------------------\n\n".join(context_parts)
        

    def _retrieve_documents(self, query: str, k: int,) -> List[Document]:
        """
        Retrieve relevant documents.
        """

        return self.retriever.retrieve(
            query=query,
            k=k,
        )
    

    def _rerank_documents(self, query: str, documents: List[Document], top_k: int,) -> List[Document]:
        """
        Rerank retrieved documents.
        """

        return self.reranker.rerank(
            query=query,
            documents=documents,
            top_k=top_k,
        )
    

    def _build_prompt(self, question: str, context: str,) -> str:
        """
        Construct the prompt for the LLM.
        """

        return self.prompt_template.format(
            question=question,
            context=context,
        )
    

    def _generate_response(self, prompt: str,) -> LLMResponse:
        """
        Generate the final response from the LLM.
        """

        return self.llm.generate(prompt)
    

    def _after_generation(self, query: str, response: LLMResponse,) -> None:
        """
        Hook that runs after the LLM generates a response.

        Subclasses can override this method.
        """
        pass

    def _determine_top_k(self) -> int:
        """
        Determine how many documents should be retrieved
        based on the LLM context window.
        """

        return self.context_strategy.get_top_k(
            self.llm.context_window,
        )


    def _get_context_token_budget(self) -> int:
        """
        Determine how many tokens can be used
        for retrieved context.
        """

        return self.token_budget_strategy.get_context_token_budget(
            self.llm.context_window,
        )
    

    def _fit_documents_to_token_budget(self, documents: List[Document], token_budget:int,) -> List[Document]:
        """
        Keep adding documents until the token budget is exhausted.
        """

        selected_documents: List[Document] = []
        remaining_budget = token_budget

        for document in documents:
            estimated_tokens = len(document.content) // 4

            if estimated_tokens <= remaining_budget:
                selected_documents.append(document)
                remaining_budget -= estimated_tokens

            else:
                break

        return selected_documents


    def run(self, query: str,) -> LLMResponse:
        if not query.strip():
            raise ValueError("Query cannot be empty.")
        
        k = self._determine_top_k()
        
        documents = self._retrieve_documents(query=query, k=k,)

        documents = self._rerank_documents(query=query, documents=documents, top_k=k,)

        token_budget = self._get_context_token_budget()

        documents = self._fit_documents_to_token_budget(
            documents=documents,
            token_budget=token_budget,
        )


        if not documents:
            context = ""
        else:
            context = self._build_context(documents,)
        
        # context = self._build_context(documents)

        prompt = self._build_prompt(question=query, context=context,)

        response = self._generate_response(prompt,)
        # llm_response = self.llm.generate(prompt)

        self._after_generation(
            query=query,
            response=response,
        )

        return response 