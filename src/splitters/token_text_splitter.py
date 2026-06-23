from typing import List

import tiktoken

from src.core.document import Document
from src.splitters.base_splitter import BaseSplitter

class TokenTextSplitter(BaseSplitter):
    """
    Splits text into chunks based on token count.
    """

    def __init__(self,chunk_size: int = 300,chunk_overlap: int = 50,):

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.encoding = tiktoken.get_encoding("cl100k_base")



    def split(self, documents: List[Document],) -> List[Document]:
        """
        Split documents into token-based chunks.
        """

        all_chunks = []

        for document in documents:

            text_chunks = self._split_text(
                document.content
            )

            for chunk in text_chunks:

                chunk_document = Document(
                    content=chunk,
                    metadata=document.metadata.copy(),
                )

                all_chunks.append(chunk_document)

        return all_chunks
    

    def _split_text(self, text: str,) -> List[str]:
        """
        Split text into token-based chunks.
        """

        tokens = self.encoding.encode(text)

        chunks = []

        start = 0

        while start < len(tokens):
            chunk_tokens = tokens[start : start + self.chunk_size]

            chunk_text = self.encoding.decode(chunk_tokens)

            chunks.append(chunk_text)

            start += (self.chunk_size - self.chunk_overlap)

        return chunks