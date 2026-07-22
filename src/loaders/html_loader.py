from bs4 import BeautifulSoup

from src.loaders.base_loader import BaseLoader
from src.core.document import Document


class HTMLLoader(BaseLoader):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator="\n", strip=True)

        documents = []

        doc = Document(
            content=text,
            metadata={
                "source": self.file_path,
                "page": 1
            }
        )

        documents.append(doc)

        return documents