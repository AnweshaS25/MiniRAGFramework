from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document


class BaseDocumentStore(ABC):
    """
    Stores original (un-chunked) documents.
    """

    @abstractmethod
    def add_documents(self, documents: List[Document],) -> None:
        pass

    @abstractmethod
    def get_documents(self, metadata_filter: dict | None = None,) -> List[Document]:
        pass


    @abstractmethod
    def get_page(self, source: str, page: int,) -> Document | None:
        """
        Return the original page corresponding
        to a source and page number.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        pass