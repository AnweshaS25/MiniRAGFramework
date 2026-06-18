from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document

class BaseSplitter(ABC):
    @abstractmethod
    def split(self, documents: List[Document]) -> List[Document]:
        pass