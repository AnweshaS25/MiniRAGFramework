import re

from typing import List

from src.core.document import Document
from src.splitters.base_splitter import BaseSplitter

class CodeSplitter(BaseSplitter):
    """
    Splits source code using classes and functions.
    """

    def split(
        self,
        documents: List[Document],
    ) -> List[Document]:

        if not documents:
            return []

        chunks = []

        pattern = r"(?=^\s*(?:class|def)\s+)"

        for document in documents:

            sections = re.split(
                pattern,
                document.content,
                flags=re.MULTILINE,
            )

            for section in sections:

                section = section.strip()

                if not section:
                    continue

                chunks.append(
                    Document(
                        content=section,
                        metadata=document.metadata.copy(),
                    )
                )

        return chunks