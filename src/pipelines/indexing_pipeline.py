from typing import List

from src.core.document import Document

from src.pipelines.base_pipeline import BasePipeline

from src.loaders.base_loader import BaseLoader
from src.splitters.base_splitter import BaseSplitter
from src.embeddings.base_embeddings import BaseEmbeddings
from src.vectorstores.base_vector_store import BaseVectorStore

class IndexingPipeline(BasePipeline):
    """
    Pipeline responsible for loading, splitting,
    embedding, and indexing documents.
    """

    def __init__(self, loader: BaseLoader, splitter: BaseSplitter, embedding_model: BaseEmbeddings, vector_store: BaseVectorStore):
        self.loader = loader
        self.splitter = splitter
        self.embedding_model = embedding_model
        self.vector_store = vector_store    


    def run(self) -> List[Document]:

        documents = self.loader.load()

        if not documents:
            raise ValueError("No documents were loaded.")

        chunks = self.splitter.split(documents)

        if not chunks:
            raise ValueError("No chunks were created.")

        chunks = self.embedding_model.embed_documents(chunks)

        self.vector_store.add_documents(chunks)

        return chunks