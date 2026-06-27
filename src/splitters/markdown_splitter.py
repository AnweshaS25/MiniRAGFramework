from typing import List
import re

from src.core.document import Document
from src.splitters.base_splitter import BaseSplitter

class MarkdownSplitter(BaseSplitter):
    """
    Splits document using markdown heading.
    """

    def split(
        self,
        documents: List[Document],
    ) -> List[Document]:

        if not documents:
            return []

        chunks = []

        heading_pattern = r"(?=^#{1,6}\s)"

        for document in documents:

            sections = re.split(
                heading_pattern,
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