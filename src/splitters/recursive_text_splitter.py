from typing import List

from src.core.document import Document
from src.splitters.base_splitter import BaseSplitter

class RecursiveTextSplitter(BaseSplitter):
    """
    Splits text recursively using progressively smaller separators.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100, separators: List[str] | None = None,):

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        if separators is None:
            self.separators = [
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        else:
            if not isinstance(separators, list):
                raise TypeError("separators must be a list of strings.")
            if not separators:
                raise ValueError("separators cannot be empty.")
            for separator in separators:
                if not isinstance(separator, str):
                    raise TypeError("All separators must be strings.")
            
            self.separators = separators



    def split(self, documents: List[Document]) -> List[Document]:
        """
        Split documents recursively into smaller chunks.
        """

        all_chunks = []

        for document in documents:
            text_chunks = self._split_text(document.content,0)

            for chunk in text_chunks:
                chunk_document = Document(content=chunk,metadata=document.metadata.copy())
                all_chunks.append(chunk_document)

        return all_chunks

    
    def _split_text(self, text: str, separator_index: int,) -> List[str]:
        """
        Recursively split text into chunks.
        """
        #BaseCase
        if len(text) <= self.chunk_size:
            return [text]
        
        #No more separators left
        if separator_index == len(self.separators) - 1:
            return self._fixed_size_split(text)
        
        separator = self.separators[separator_index]
        pieces = text.split(separator)

        result = []

        for piece in pieces:

            piece = piece.strip()

            if not piece:
                continue

            if len(piece) <= self.chunk_size:
                result.append(piece)

            else:
                recursive_chunks = self._split_text(piece,separator_index + 1)

                result.extend(recursive_chunks)

        return self._merge_chunks(result)
        

    def _fixed_size_split(self, text: str,) -> List[str]:
        """
        Split text into fixed-size chunks as a last resort.
        """

        chunks = []
        start = 0

        while start < len(text):

            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap

        return chunks
    

    def _merge_chunks(self, chunks: List[str],) -> List[str]:
        """
        Merge adjacent chunks while respecting chunk_size.
        """

        merged = []
        current_chunk = ""

        for chunk in chunks:

            if not current_chunk:
                current_chunk = chunk

            else:

                candidate = current_chunk + "\n\n" + chunk

                if len(candidate) <= self.chunk_size:
                    current_chunk = candidate

                else:
                    merged.append(current_chunk)
                    current_chunk = chunk

        if current_chunk:
            merged.append(current_chunk)

        return merged
