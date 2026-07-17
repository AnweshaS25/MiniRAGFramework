from src.constants import PromptRouterTypes
from src.constants import ToolRouterTypes
from src.constants import ContextRouterTypes
from src.constants import QueryRewriterTypes

from dataclasses import dataclass


@dataclass
class FrameworkConfig:
    """
    Stores the configuration required to build
    a MiniRAG framework.
    """

    loader_type: str
    splitter_type: str
    embedding_type: str
    vector_store_type: str
    retriever_type: str

    llm_types: list[str]
    
    prompt_router_type: PromptRouterTypes

    tool_router_type: ToolRouterTypes

    context_router_type: ContextRouterTypes

    query_rewriter_type: QueryRewriterTypes

    conversation_window_size: int = 2

    summarize_after: int = 6
