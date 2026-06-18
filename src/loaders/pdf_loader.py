import fitz 

from src.loaders.base_loader import BaseLoader
from src.core.document import Document


class PDFLoader(BaseLoader):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        pdf = fitz.open(self.file_path)  #This does NOT extract any text. It simply opens the PDF.
        documents = []

        for page_num, page in enumerate(pdf):   #Visit every page in the PDF; each iteration gives a page object; enumerate for indexing 
            text = page.get_text() #extract the text from a page. This will be the content in the document object; type of text is string

            doc = Document(
                content=text,
                metadata={
                "source": self.file_path,
                "page": page_num + 1      #since enumerate does indexing from 0
                }
            )

            documents.append(doc)

        return documents

    