from typing import List

from src.core.document import Document
from src.splitters.base_splitter import BaseSplitter

class SentenceSplitter(BaseSplitter):
    """
    Splits documents at sentence boundaries.
    """

    def __init__(self,
                 chunk_size: int =5,
                 ):
            self.chunk_size=chunk_size

    def split(self, documents: List[Document],
        )-> List[Document]:
          
          if not documents:
                return[]
          
          chunks=[]

          for document in documents:
                sentences=[
                      sentence.strip()
                      for sentence in document.content.split(".")
                      if sentence.strip()
                ]

                for i in range(
                      0,
                      len(sentences),
                      self.chunk_size,
                ):
                      sentence_group= sentences[
                            i:i+ self.chunk_size
                      ]
                      chunk_text=". ".join(sentence_group)

                      chunks.append(
                            Document( content=chunk_text, metadata=document.metadata.copy(),
                                     )
                      )

                return chunks