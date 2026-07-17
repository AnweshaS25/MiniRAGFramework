class FrameworkComponents:
    """
    Container for all components built by the framework.
    """

    def __init__(self):

        self.core = None

        self.llm_manager = None

        self.memory = None

        self.prompt_manager = None

        self.tool_manager = None

        self.security_guard = None

        self.output_guard = None

        self.context_manager = None

        self.query_rewriter = None

        self.memory_retriever = None

        self.reranker = None