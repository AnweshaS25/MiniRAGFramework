from abc import ABC, abstractmethod   #ABC: Abstract Base Class
from typing import List

from src.core.document import Document


class BaseLoader(ABC):

    @abstractmethod
    def load(self) -> List[Document]:  #This function returns a list of Document objects.
        """
        Load documents and return a list of Document objects.
        """
        pass
