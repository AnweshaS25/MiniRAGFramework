from src.pipelines.conversational_rag_pipeline import ConversationalRAGPipeline


class PipelineBuilder:
    """
    Builds the RAG pipeline.
    """

    def __init__(self, config):

        self.config = config

    def build(
        self,
        components,
    ):
        pass