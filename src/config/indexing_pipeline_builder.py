from src.pipelines.indexing_pipeline import IndexingPipeline
from src.document_store.in_memory_document_store import (
    InMemoryDocumentStore,
)


class IndexingPipelineBuilder:
    """
    Builds the indexing pipeline.
    """

    def __init__(self, config):

        self.config = config

    def build(
        self,
        core,
    ):
        document_store = InMemoryDocumentStore()

        indexing_pipeline = IndexingPipeline(
            loader=core["loader"],
            splitter=core["splitter"],
            embedding_model=core["embedding_model"],
            vector_store=core["vector_store"],
            document_store=document_store,
        )

        return {
            "document_store": document_store,
            "indexing_pipeline": indexing_pipeline,
        }