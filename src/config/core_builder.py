from src.config.framework_config import FrameworkConfig

from src.factories.loader_factory import LoaderFactory
from src.factories.splitter_factory import SplitterFactory
from src.factories.embedding_factory import EmbeddingFactory
from src.factories.vector_store_factory import VectorStoreFactory
from src.factories.retriever_factory import RetrieverFactory


class CoreBuilder:
    """
    Builds the core retrieval components
    of the MiniRAG framework.
    """

    def __init__(self, config: FrameworkConfig):

        self.config = config

    def build_core(
        self,
        file_path: str,
    ):

        loader = LoaderFactory.create(
            self.config.loader_type,
            file_path=file_path,
        )

        splitter = SplitterFactory.create(
            self.config.splitter_type,
        )

        embedding_model = EmbeddingFactory.create(
            self.config.embedding_type,
        )

        vector_store = VectorStoreFactory.create(
            self.config.vector_store_type,
            persist_directory=self.config.persist_directory,
        )

        retriever = RetrieverFactory.create(
            self.config.retriever_type,
            embedding_model=embedding_model,
            vector_store=vector_store,
        )

        return {
            "loader": loader,
            "splitter": splitter,
            "embedding_model": embedding_model,
            "vector_store": vector_store,
            "retriever": retriever,
        }