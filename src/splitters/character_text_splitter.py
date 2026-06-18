from src.splitters.base_splitter import BaseSplitter
from src.core.document import Document
from typing import List

class CharacterTextSplitter(BaseSplitter):
    
    def __init__(self, chunk_size: int, chunk_overlap: int):

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, documents: List[Document]) -> List[Document]:

        all_chunks = []

        for doc in documents:

            text = doc.content

            start = 0

            while start < len(text):

                chunk = text[start : start + self.chunk_size]

                chunk_document = Document(
                    content=chunk,
                    metadata=doc.metadata.copy()
                )
                
                all_chunks.append(chunk_document)

                start += self.chunk_size - self.chunk_overlap

        return all_chunks