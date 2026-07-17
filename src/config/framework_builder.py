from src.config.framework_config import FrameworkConfig
from src.config.core_builder import CoreBuilder
from src.config.llm_builder import LLMBuilder

from src.config.framework_components import FrameworkComponents

from src.config.memory_builder import MemoryBuilder

from src.config.prompt_builder import PromptBuilder

from src.config.tool_builder import ToolBuilder

from src.config.context_builder import ContextBuilder

from src.config.query_builder import QueryBuilder

from src.config.security_builder import SecurityBuilder

from src.config.indexing_pipeline_builder import IndexingPipelineBuilder


class FrameworkBuilder:
    """
    Coordinates all builders required to
    construct a MiniRAG framework.
    """

    def __init__(self, config: FrameworkConfig):

        if config is None:
            raise ValueError("config cannot be None.")

        self.config = config

        self.components = FrameworkComponents()

        self.core_builder = CoreBuilder(config)
        self.llm_builder = LLMBuilder(config)

        self.memory_builder = MemoryBuilder(config)

        self.prompt_builder = PromptBuilder(config)

        self.tool_builder = ToolBuilder(config)

        self.context_builder = ContextBuilder(config)

        self.query_builder = QueryBuilder(config)

        self.security_builder = SecurityBuilder(config)

        self.indexing_pipeline_builder = IndexingPipelineBuilder(config)


    def build_core(
        self,
        file_path: str,
    ):
        """
        Build the core retrieval components.
        """

        return self.core_builder.build_core(
            file_path=file_path,
        )
    

    def build_llm(self):
        """
        Build the LLM manager.
        """

        return self.llm_builder.build()
    

    def build(
        self,
        file_path: str,
    ):
        """
        Build the framework and return all components.
        """

        self.components.core = self.build_core(
            file_path,
        )

        self.components.llm_manager = self.build_llm()

        self.components.memory = self.build_memory()

        self.components.prompt_manager = self.build_prompt_manager()

        self.components.tool_manager = self.build_tool_manager()

        self.components.context_manager = self.build_context_manager()

        query_components = self.build_query()

        self.components.query_rewriter = query_components["query_rewriter"]

        self.components.memory_retriever = query_components["memory_retriever"]

        security_components = self.build_security()
        
        self.components.security_guard = security_components["security_guard"]
        self.components.output_guard = security_components["output_guard"]
        self.components.token_budget_strategy = security_components["token_budget_strategy"]
        self.components.reranker = security_components["reranker"]

        indexing_components = self.build_indexing_pipeline()

        self.components.document_store = indexing_components["document_store"]

        self.components.indexing_pipeline = indexing_components["indexing_pipeline"]

        return self.components
    

    def build_memory(self):
        return self.memory_builder.build(
            llm_manager=self.components.llm_manager,
        )
    

    def build_prompt_manager(self):
        return self.prompt_builder.build(
            llm_manager=self.components.llm_manager,
        )
    

    def build_tool_manager(self):
        return self.tool_builder.build(
            llm_manager=self.components.llm_manager,
        )
    

    def build_context_manager(self):
        return self.context_builder.build(
            llm_manager=self.components.llm_manager,
        )
    

    def build_query(self):
        return self.query_builder.build(
            llm_manager=self.components.llm_manager,
        )
    

    def build_security(self):
        return self.security_builder.build(
            llm_manager=self.components.llm_manager,
        )
    

    def build_indexing_pipeline(self):
        return self.indexing_pipeline_builder.build(
            core=self.components.core,
        )