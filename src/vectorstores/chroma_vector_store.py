from typing import List
import uuid

import chromadb

from src.core.document import Document
from src.vectorstores.base_vector_store import BaseVectorStore


class ChromaVectorStore(BaseVectorStore):
    """
    Persistent vector store backed by ChromaDB.
    """

    def __init__(self, collection_name: str = "documents", persist_directory: str = "./chroma_db",):
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        try:
            self._client = chromadb.PersistentClient(path=self.persist_directory)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize ChromaDB: {e}")
        
        try:
            self._collection = self._client.get_or_create_collection(name=self.collection_name)
        except Exception as e:
            raise RuntimeError(f"Failed to access collection '{self.collection_name}': {e}")
        

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents and their embeddings to the Chroma collection.
        """

        if not documents:
            raise ValueError("documents cannot be empty.")

        ids = []
        texts = []
        embeddings = []
        metadatas = []

        for document in documents:
            embedding = document.embedding

            if embedding is None:
                raise ValueError("All documents must have embeddings before they can be added to the vector store.")
                
                
            doc_id = str(uuid.uuid4())     #Framework owns the IDs.

            ids.append(doc_id)
            texts.append(document.content)
            embeddings.append(list(embedding))
            metadatas.append(document.metadata)

        try:
            self._collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas,)
        except Exception as e:
            raise RuntimeError(f"Failed to add documents to collection '{self.collection_name}': {e}")
            

    def similarity_search(self, query_embedding: List[float], k: int,) -> List[Document]:
        """
        Return the k most similar documents.
        """
        if not query_embedding:
            raise ValueError("query_embedding cannot be empty.")

        if k <= 0:
            raise ValueError("k must be greater than 0.")
        
        try:
            results = self._collection.query(query_embeddings=[query_embedding], n_results=k,)
        except Exception as e:
            raise RuntimeError(f"Failed to perform similarity search: {e}")
        
        if not results["documents"][0]:
            return []
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0] or [{} for _ in documents]

        #Converting back to document object
        retrieved_documents = []

        for content, metadata in zip(documents, metadatas):
            retrieved_documents.append(
                Document(content=content,metadata=metadata,)
            )

        return retrieved_documents
    

    def clear(self) -> None:
        """
        Removes all documents from the collection.
        """

        try:
            self._client.delete_collection(
                name=self.collection_name
            )

            self._collection = self._client.get_or_create_collection(
                name=self.collection_name
            )

        except Exception as e:
            raise RuntimeError(
                f"Failed to clear collection '{self.collection_name}': {e}"
            )