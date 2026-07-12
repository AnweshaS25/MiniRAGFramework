from typing import List

from src.core.document import Document
from src.document_store.base_document_store import BaseDocumentStore


class InMemoryDocumentStore(BaseDocumentStore):
    """
    Stores original documents in memory.
    """

    def __init__(self):
        self._documents = []

    def add_documents(self, documents: List[Document],) -> None:
        self._documents.extend(documents)

    def get_documents(self, metadata_filter: dict | None = None,) -> List[Document]:
        if metadata_filter is None:
            return list(self._documents)

        filtered = []

        for document in self._documents:
            matches = True
            for key, value in metadata_filter.items():
                if document.metadata.get(key) != value:
                    matches = False
                    break

            if matches:
                filtered.append(document)

        return filtered
    

    def get_page(self, source: str, page: int,) -> Document | None:

        for document in self._documents:

            if (
                document.metadata.get("source") == source
                and
                document.metadata.get("page") == page
            ):
                return document

        return None


    def clear(self):

        self._documents.clear()