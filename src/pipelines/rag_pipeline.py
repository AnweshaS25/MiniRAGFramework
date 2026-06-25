from typing import List

from src.core.document import Document
from src.core.llm_response import LLMResponse

from src.pipelines.base_pipeline import BasePipeline

from src.retrievers.base_retriever import BaseRetriever
from src.prompts.base_prompt_template import BasePromptTemplate
from src.llms.base_llm import BaseLLM


class RAGPipeline(BasePipeline):
    """
    Pipeline responsible for retrieving relevant documents,
    constructing the prompt, and generating the final answer.
    """

    def __init__(self, retriever: BaseRetriever, prompt_template: BasePromptTemplate,llm: BaseLLM,):
        self.retriever = retriever
        self.prompt_template = prompt_template
        self.llm = llm

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


    def run(self, query: str, k: int = 3,) -> LLMResponse:
        if not query.strip():
            raise ValueError("Query cannot be empty.")
        
        documents = self._retrieve_documents(query=query, k=k,)

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