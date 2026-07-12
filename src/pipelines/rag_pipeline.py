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

from src.security.base_guard import BaseGuard

from src.auth.user import User
from src.auth.metadata_filter_builder import MetadataFilterBuilder

from src.tools.tool_manager import ToolManager
from src.prompts.prompt_manager import PromptManager

from src.strategies.context_manager import ContextManager


class RAGPipeline(BasePipeline):
    """
    Pipeline responsible for retrieving relevant documents,
    constructing the prompt, and generating the final answer.
    """

    def __init__(self, retriever: BaseRetriever, prompt_manager, document_store,llm_manager, reranker: BaseReranker, context_manager,token_budget_strategy: BaseTokenBudgetStrategy, security_guard: BaseGuard, output_guard, tool_manager: ToolManager,):

        if retriever is None:
            raise ValueError("retriever cannot be None.")

        if prompt_manager is None:
            raise ValueError("prompt_template cannot be None.")

        if llm_manager is None:
            raise ValueError("llm cannot be None.")

        if reranker is None:
            raise ValueError("reranker cannot be None.")
        
        if context_manager is None:
            raise ValueError("context_manager cannot be None.")
        
        if token_budget_strategy is None:
            raise ValueError("token_budget_strategy cannot be None.")
        
        if security_guard is None:
            raise ValueError("security_guard cannot be None.")
        
        if output_guard is None:
            raise ValueError("output_guard cannot be None.")
        
        if tool_manager is None:
            raise ValueError("tool_manager cannot be None.")

        self.retriever = retriever
        self.prompt_manager = prompt_manager
        self.document_store = document_store
        self.llm_manager = llm_manager
        self.reranker = reranker
        self.context_manager = context_manager
        self.token_budget_strategy = token_budget_strategy
        self.security_guard = security_guard
        self.output_guard = output_guard
        self.tool_manager = tool_manager

    # def _build_context(self, documents: List[Document],) -> str:
    #     context_parts = []

    #     for document in documents:
    #         source = document.metadata.get("source", "Unknown")
    #         page = document.metadata.get("page", "Unknown")

    #         context_parts.append(
    #             f"Source: {source}\n"
    #             f"Page: {page}\n\n"
    #             f"{document.content}"
    #         )

    #     return "\n\n----------------------------------------\n\n".join(context_parts)
        

    def _retrieve_documents(self, query: str, user: User, k: int,) -> List[Document]:
        """
        Retrieve relevant documents.
        """

        metadata_filter = MetadataFilterBuilder.build(user)


        return self.retriever.retrieve(
            query=query,
            k=k,
            metadata_filter=metadata_filter,
        )


    def _load_full_documents(self, user: User,) -> List[Document]:
        """
        Loads the original documents from the Document Store.
        """

        return self.document_store.get_documents()
    

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

    def _determine_top_k(self, query: str, llm, context_strategy,) -> int:
        """
        Determine how many documents should be retrieved
        based on the LLM context window.
        """

        # context_strategy = self.context_manager.get_strategy(query)

        return context_strategy.get_top_k(
            llm.context_window,
        )
    

    def _validate_query(self, query: str) -> None:
        """
        Validate the user query before retrieval.
        """

        security_result = self.security_guard.validate(query)

        if not security_result.safe:
            raise ValueError(
                security_result.reason
            )


    def _get_context_token_budget(self, llm) -> int:
        """
        Determine how many tokens can be used
        for retrieved context.
        """

        return self.token_budget_strategy.get_context_token_budget(
            llm.context_window,
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
    


    def run(self, query: str, user: User,) -> LLMResponse:
        if not query.strip():
            raise ValueError("Query cannot be empty.")
        
        self._validate_query(query)

        context_strategy = self.context_manager.get_strategy(query)

        tool_used, tool_result = self.tool_manager.process(
            user_query=query,
            query=query,      # passed as kwargs to tools
        )

        if tool_used:

            tool_prompt = f"""
        The user asked:

        {query}

        The following is the output from a tool:

        {tool_result}

        Answer the user naturally using this tool output.

        Do not mention that a tool was used.
        """
            
            tool_response = self.llm_manager.get_llm(query).generate(tool_prompt)

            return tool_response
        
        llm = self.llm_manager.get_llm(query)
        

        if context_strategy.requires_retrieval():

            original_documents = None

            k = self._determine_top_k(
                query=query,
                llm=llm,
                context_strategy=context_strategy,
            )
        
            documents = self._retrieve_documents(
                query=query, 
                user=user, 
                k=k,
            )

            documents = self._rerank_documents(
                query=query, 
                documents=documents, 
                top_k=k,
            )

            if context_strategy.name == "hybrid":
                print("Loading original documents for Hybrid Mode")
                original_documents = self._load_full_documents(user)

        else:
            print("Using Document Store (LCM Mode)")
            documents = self._load_full_documents(user)
            original_documents = None



        token_budget = self._get_context_token_budget(llm)

        documents = self._fit_documents_to_token_budget(
            documents=documents,
            token_budget=token_budget,
        )


        if not documents:
            raise PermissionError(
                "You do not have permission to access any relevant documents."
            )

        context = context_strategy.build_context(
            retrieved_chunks=documents,
            original_documents=original_documents,
        )
        
        # context = self._build_context(documents)

        prompt_template = self.prompt_manager.get_prompt_template(query)

        prompt = prompt_template.format(
            question=query,
            context=context,
            history="",
        )

        llm_chain = self.llm_manager.get_llm_chain(query)

        last_exception = None

        for llm in llm_chain:
            print(f"Trying {llm.__class__.__name__}...")

            try:
                response = llm.generate(prompt)
                print(f"Using {llm.__class__.__name__}")
                break

            except Exception as e:
                print(f"{llm.__class__.__name__} failed: {e}")
                last_exception = e

        else:
            raise RuntimeError(
                f"All registered LLMs failed. Last error: {last_exception}"
            )

        # response = llm.generate(prompt)

        # response = self._generate_response(prompt)
        # llm_response = self.llm.generate(prompt)

        output_result = self.output_guard.validate(response.text,)

        if not output_result.safe:
            raise ValueError(output_result.reason)

        self._after_generation(
            query=query,
            response=response,
        )

        return response