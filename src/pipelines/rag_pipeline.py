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
        

    def run(self, query: str, k: int = 3,) -> LLMResponse:
        if not query.strip():
            raise ValueError("Query cannot be empty.")
        
        documents = self.retriever.retrieve(query=query, k=k)

        if not documents:
            context = ""
        else:
            context = self._build_context(documents)
        
        # context = self._build_context(documents)

        prompt = self.prompt_template.format(question=query, context=context)

        llm_response = self.llm.generate(prompt)

        return llm_response