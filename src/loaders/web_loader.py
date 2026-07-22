import requests
from bs4 import BeautifulSoup

from src.loaders.base_loader import BaseLoader
from src.core.document import Document


class WebLoader(BaseLoader):

    def __init__(self, url: str):
        self.url = url

    def load(self):
        response = requests.get(self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator="\n", strip=True)

        documents = []

        doc = Document(
            content=text,
            metadata={
                "source": self.url,
                "page": 1
            }
        )

        documents.append(doc)

        return documents