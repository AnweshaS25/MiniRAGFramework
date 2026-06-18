from typing import List

from sentence_transformers import SentenceTransformer

from src.embeddings.base_embeddings import BaseEmbeddings
from src.core.document import Document


class HuggingFaceEmbeddings(BaseEmbeddings):
    """
    Embedding model using Hugging Face Sentence Transformers.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):

        if not isinstance(model_name, str):
            raise TypeError("model_name must be a string.")

        if not model_name.strip():
            raise ValueError("model_name cannot be empty.")

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: List[Document]) -> List[Document]:

        if not documents:
            return []

        texts = [
            document.content
            for document in documents
        ]

        embeddings = self.model.encode(texts, convert_to_numpy=True)

        for document, embedding in zip(documents, embeddings):
            document.embedding = embedding.tolist()

        return documents